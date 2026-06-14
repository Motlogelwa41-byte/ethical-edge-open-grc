def ingest_king_v_framework(framework_data, session, tenant_id):
    # If the root is a list, wrap it in a dummy dict structure to keep your logic working
    if isinstance(framework_data, list):
        # Assuming the list contains categories
        framework_data = {"governing_functions": {f"cat_{i}": item for i, item in enumerate(framework_data)}}
    
    categories = framework_data.get("governing_functions", {})
    # ... rest of your code ...

import os
import json
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text

def ingest_king_v_framework(framework_data: Dict[str, Any], session: Session, tenant_id: str):
    print(f"🚀 Injecting framework for Tenant: {tenant_id}")
    
    categories = framework_data.get("governing_functions", {})
    
    for category_key, category_content in categories.items():
        # 1. Upsert Category
        session.execute(
            text("""
                INSERT INTO compliance_categories (category_id, display_name, weight, tenant_id)
                VALUES (:category_id, :display_name, :weight, :tenant_id)
                ON CONFLICT (category_id, tenant_id) DO UPDATE SET
                    display_name = EXCLUDED.display_name,
                    weight = EXCLUDED.weight;
            """),
            {"category_id": category_key, "display_name": category_content.get("title"), 
             "weight": category_content.get("weight", 1.0), "tenant_id": tenant_id}
        )
        
        # 2. Upsert Principles
        for principle in category_content.get("principles", []):
            p_id = principle.get("principle_id")
            session.execute(
                text("""
                    INSERT INTO compliance_principles (principle_id, category_id, title, description, tenant_id)
                    VALUES (:principle_id, :category_id, :title, :description, :tenant_id)
                    ON CONFLICT (principle_id, tenant_id) DO UPDATE SET
                        title = EXCLUDED.title, description = EXCLUDED.description;
                """),
                {"principle_id": p_id, "category_id": category_key, "title": principle.get("title"), 
                 "description": principle.get("description"), "tenant_id": tenant_id}
            )
            
            # 3. Upsert Gates
            for index, gate in enumerate(principle.get("checkpoints_or_gates", [])):
                gate_id = f"GATE-{p_id}-{str(index + 1).zfill(2)}"
                session.execute(
                    text("""
                        INSERT INTO room_gates (gate_id, principle_id, requirement_text, validation_type, order_index, tenant_id)
                        VALUES (:gate_id, :principle_id, :requirement_text, :validation_type, :order_index, :tenant_id)
                        ON CONFLICT (gate_id, tenant_id) DO UPDATE SET
                            requirement_text = EXCLUDED.requirement_text;
                    """),
                    {"gate_id": gate_id, "principle_id": p_id, "requirement_text": gate.get("requirement"), 
                     "validation_type": gate.get("type", "automated"), "order_index": index, "tenant_id": tenant_id}
                )
    session.commit()

if __name__ == "__main__":
    from app.database.connection import SessionLocal
    
    # Ensure the data file exists
    data_path = 'data/king_v_checklist.json'
    if not os.path.exists(data_path):
        print(f"❌ Error: File not found at {data_path}")
    else:
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        db = SessionLocal()
        try:
            tenant_id = os.getenv("TARGET_TENANT_ID")
            if not tenant_id:
                print("❌ Error: TARGET_TENANT_ID environment variable not set.")
            else:
                ingest_king_v_framework(data, db, tenant_id)
                print("✅ Ingestion successfully completed!")
        except Exception as e:
            print(f"❌ Critical Pipeline Failure: {e}")
        finally:
            db.close()
