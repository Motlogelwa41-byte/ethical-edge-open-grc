import os
import json
import sqlite3  # Using standard sqlite3 for local development/testing; easily interchangeable with psycopg2 for Postgres
from typing import Dict, Any

# Path configurations relative to the repository core
CHECKLIST_PATH = os.path.join("data", "king_v_checklist.json")
DB_PATH = os.path.join("database", "local_grc.db")  # Set via environment variables in production

def load_framework_source(file_path: str) -> Dict[str, Any]:
    """
    Safely opens and loads the JSON compliance mapping file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target framework definition not found at: {file_path}")
        
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def initialize_database_connection(db_path: str) -> sqlite3.Connection:
    """
    Establishes a connection to the local database perimeter.
    """
    conn = sqlite3.connect(db_path)
    # Enable foreign key support inside SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def ingest_king_v_framework(framework_data: Dict[str, Any], conn: sqlite3.Connection):
    """
    Parses the framework data and injects it into relational schema records.
    Handles upserts cleanly so the script can be rerun without breaking constraints.
    """
    cursor = conn.cursor()
    
    print(f"🚀 Initializing ingestion for framework: {framework_data.get('framework_name', 'King V')}")
    
    # 1. Ingest Top-Level Governing Functions / Categories
    categories = framework_data.get("governing_functions", {})
    
    for category_key, category_content in categories.items():
        # Ensure category exists in your relational layout
        cursor.execute("""
            INSERT INTO compliance_categories (category_id, display_name, weight)
            VALUES (?, ?, ?)
            ON CONFLICT(category_id) DO UPDATE SET
                display_name=excluded.display_name,
                weight=excluded.weight;
        """, (category_key, category_content.get("title"), category_content.get("weight", 1.0)))
        
        # 2. Extract and Ingest Principles belonging to this category
        principles = category_content.get("principles", [])
        for principle in principles:
            p_id = principle.get("principle_id")
            
            cursor.execute("""
                INSERT INTO compliance_principles (principle_id, category_id, title, description)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(principle_id) DO UPDATE SET
                    category_id=excluded.category_id,
                    title=excluded.title,
                    description=excluded.description;
            """, (p_id, category_key, principle.get("title"), principle.get("description")))
            
            # 3. Extract and Build the Gate Requirements (The core tracking checkpoints)
            gates = principle.get("checkpoints_or_gates", [])
            for index, gate in enumerate(gates):
                # Formulate a structured unique gate ID (e.g., GATE-P1-01)
                gate_id = f"GATE-{p_id}-{str(index + 1).zfill(2)}"
                
                cursor.execute("""
                    INSERT INTO room_gates (gate_id, principle_id, requirement_text, validation_type, order_index)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(gate_id) DO UPDATE SET
                        requirement_text=excluded.requirement_text,
                        validation_type=excluded.validation_type,
                        order_index=excluded.order_index;
                """, (
                    gate_id, 
                    p_id, 
                    gate.get("requirement"), 
                    gate.get("type", "automated"), # 'automated' or 'manual_upload'
                    index
                ))
                
    conn.commit()
    print("✅ Framework data pipeline integration complete. Room gates are armed.")

def main():
    try:
        # Load the configuration raw components
        raw_framework = load_framework_source(CHECKLIST_PATH)
        
        # Connect to your operational database layer
        db_connection = initialize_database_connection(DB_PATH)
        
        # Execute the map-injection pipeline
        ingest_king_v_framework(raw_framework, db_connection)
        
        db_connection.close()
        
    except Exception as e:
        print(f"❌ Critical Data Pipeline Failure: {str(e)}")

if __name__ == "__main__":
    main()
