import os
import json
import psycopg2
from psycopg2.extras import execute_values
from typing import Dict, Any

# Path configuration relative to repository core
CHECKLIST_PATH = os.path.join("data", "king_v_checklist.json")

def load_environment_credentials() -> Dict[str, str]:
    """
    Ensures database connection variables are pulled directly 
    from the environment configuration perimeter.
    """
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return {"dsn": db_url}
        
    # Fallback mapping if individual environment flags are used in docker-compose.yml
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "ethical_edge_grc"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "securepassword"),
        "port": os.getenv("DB_PORT", "5432")
    }

def load_framework_source(file_path: str) -> Dict[str, Any]:
    """Safely loads the JSON compliance mapping configuration."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target framework definition not found at: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def ingest_king_v_framework(framework_data: Dict[str, Any], conn):
    """
    Parses the framework tree structure and executes batch upserts 
    into production PostgreSQL tables 11, 12, and 13.
    """
    with conn.cursor() as cursor:
        print(f"🚀 Launching production pipeline for: {framework_data.get('framework_name', 'King V')}")
        
        categories = framework_data.get("governing_functions", {})
        
        for category_key, category_content in categories.items():
            # 1. Upsert Governing Categories (Table 11)
            cursor.execute("""
                INSERT INTO compliance_categories (category_id, display_name, weight)
                VALUES (%s, %s, %s)
                ON CONFLICT (category_id) DO UPDATE SET
                    display_name = EXCLUDED.display_name,
                    weight = EXCLUDED.weight;
            """, (category_key, category_content.get("title"), category_content.get("weight", 1.0)))
            
            principles = category_content.get("principles", [])
            for principle in principles:
                p_id = principle.get("principle_id")
                
                # 2. Upsert the 13 King V Principles (Table 12)
                cursor.execute("""
                    INSERT INTO compliance_principles (principle_id, category_id, title, description)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (principle_id) DO UPDATE SET
                        category_id = EXCLUDED.category_id,
                        title = EXCLUDED.title,
                        description = EXCLUDED.description;
                """, (p_id, category_key, principle.get("title"), principle.get("description")))
                
                gates = principle.get("checkpoints_or_gates", [])
                for index, gate in enumerate(gates):
                    gate_id = f"GATE-{p_id}-{str(index + 1).zfill(2)}"
                    
                    # 3. Upsert Operational Room Gates Checkpoints (Table 13)
                    cursor.execute("""
                        INSERT INTO room_gates (gate_id, principle_id, requirement_text, validation_type, order_index)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (gate_id) DO UPDATE SET
                            requirement_text = EXCLUDED.requirement_text,
                            validation_type = EXCLUDED.validation_type,
                            order_index = EXCLUDED.order_index;
                    """, (
                        gate_id,
                        p_id,
                        gate.get("requirement"),
                        gate.get("type", "automated"),
                        index
                    ))
                    
        conn.commit()
        print("✅ Production database framework injection complete. Global room grids are armed.")

def main():
    conn = None
    try:
        # Load framework content definitions
        raw_framework = load_framework_source(CHECKLIST_PATH)
        
        # Pull environment configurations
        db_config = load_environment_credentials()
        
        # Connect directly to your PostgreSQL engine container
        if "dsn" in db_config:
            conn = psycopg2.connect(db_config["dsn"])
        else:
            conn = psycopg2.connect(**db_config)
            
        ingest_king_v_framework(raw_framework, conn)
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Critical Production Pipeline Failure: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
