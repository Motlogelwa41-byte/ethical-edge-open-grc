import os
import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any

# Assuming database.connection exposes your engine session creator
from database.connection import get_db_session

CHECKLIST_PATH = os.path.join("data", "king_v_checklist.json")

def load_framework_source(file_path: str) -> Dict[str, Any]:
    """Safely loads the JSON compliance mapping configuration."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target framework definition not found at: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def ingest_king_v_framework(framework_data: Dict[str, Any], session: Session):
    """
    Parses the framework tree structure and executes batch upserts 
    using SQLAlchemy text blocks matching your production init_schema.sql.
    """
    print(f"🚀 Launching database engine injection loop for: {framework_data.get('framework_name', 'King V')}")
    
    categories = framework_data.get("governing_functions", {})
    
    # Use explicit text mappings to interface smoothly with raw init_schema.sql tables
    for category_key, category_content in categories.items():
        # 1. Upsert Governing Categories
        session.execute(
            text("""
                INSERT INTO compliance_categories (category_id, display_name, weight)
                VALUES (:category_id, :display_name, :weight)
                ON CONFLICT (category_id) DO UPDATE SET
                    display_name = EXCLUDED.display_name,
                    weight = EXCLUDED.weight;
            """),
            {"category_id": category_key, "display_name": category_content.get("title"), "weight": category_content.get("weight", 1.0)}
        )
        
        principles = category_content.get("principles", [])
        for principle in principles:
            p_id = principle.get("principle_id")
            
            # 2. Upsert the 13 King V Principles
            session.execute(
                text("""
                    INSERT INTO compliance_principles (principle_id, category_id, title, description)
                    VALUES (:principle_id, :category_id, :title, :description)
                    ON CONFLICT (principle_id) DO UPDATE SET
                        category_id = EXCLUDED.category_id,
                        title = EXCLUDED.title,
                        description = EXCLUDED.description;
                """),
                {"principle_id": p_id, "category_id": category_key, "title": principle.get("title"), "description": principle.get("description")}
            )
            
            gates = principle.get("checkpoints_or_gates", [])
            for index, gate in enumerate(gates):
                gate_id = f"GATE-{p_id}-{str(index + 1).zfill(2)}"
                
                # 3. Upsert Operational Room Gates Checkpoints
                session.execute(
                    text("""
                        INSERT INTO room_gates (gate_id, principle_id, requirement_text, validation_type, order_index)
                        VALUES (:gate_id, :principle_id, :requirement_text, :validation_type, :order_index)
                        ON CONFLICT (gate_id) DO UPDATE SET
                            requirement_text = EXCLUDED.requirement_text,
                            validation_type = EXCLUDED.validation_type,
                            order_index = EXCLUDED.order_index;
                    """),
                    {
                        "gate_id": gate_id,
                        "principle_id": p_id,
                        "requirement_text": gate.get("requirement"),
                        "validation_type": gate.get("type", "automated"),
                        "order_index": index
                    }
                )
                
    session.commit()
    print("✅ Ingestion pipeline sync complete. Relational constraints updated smoothly.")

def main():
    # Use your defined dependency generator to open a secure db boundary session
    db_generator = get_db_session()
    session = next(db_generator)
    
    try:
        raw_framework = load_framework_source(CHECKLIST_PATH)
        ingest_king_v_framework(raw_framework, session)
    except Exception as e:
        session.rollback()
        print(f"❌ Critical Production Pipeline Failure: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    main()

def ingest_king_v_framework(framework_data: Dict[str, Any], session: Session, tenant_id: str):
    # ... (Keep your current logic)
    
    # Update your INSERT statements to include the tenant_id
    # Example:
    session.execute(
        text("""
            INSERT INTO compliance_categories (category_id, display_name, weight, tenant_id)
            VALUES (:category_id, :display_name, :weight, :tenant_id)
            ON CONFLICT (category_id, tenant_id) DO UPDATE SET ...
        """),
        {..., "tenant_id": tenant_id}
    )
