"""
Ethical Edge Open GRC Engine
File: ingest_frameworks.py
Objective: Validates and loads GRC compliance frameworks (UNICEF & King V) into relational storage.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, ValidationError

from sqlalchemy import text
from app.database.session import SessionLocal

# ==========================================
# 1. PYDANTIC VALIDATION SCHEMAS
# ==========================================

class FrameworkRequirement(BaseModel):
    id: str
    requirement_text: str
    validation_type: str = "automated"

class Category(BaseModel):
    title: str
    weight: float = 1.0
    principles: List[Dict[str, Any]] = []

# ==========================================
# 2. UNICEF INGESTION MODULE
# ==========================================

def ingest_unicef_safeguarding_framework():
    """
    Reads the unicef_child_safeguarding.json config file
    and registers the controls into the database tracking system.
    """
    print("📥 Ingesting UNICEF Child Safeguarding Framework...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "unicef_child_safeguarding.json")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: Configuration file missing at {file_path}")
        return

    with open(file_path, "r") as f:
        framework_data = json.load(f)

    print(f"✅ Successfully parsed: {framework_data.get('framework_name')} (v{framework_data.get('version')})")
    print(f"   Loaded {len(framework_data.get('compliance_sections', []))} regulatory sections.")
    
    # Note: Connect this execution layer to your SQLAlchemy session if tracking via DB models.

# ==========================================
# 3. KING V & GENERAL INGESTION MODULES
# ==========================================

def ingest_king_v_framework(framework_data: Any, tenant_id: str = "DEMO_TENANT"):
    """
    Parses structural framework dicts/lists, validates data integrity thresholds,
    and upserts categories, principles, and checkpoints safely via raw SQL executions.
    """
    db = SessionLocal()
    
    # Standardize incoming lists or dictionaries safely
    if isinstance(framework_data, list):
        categories = {f"cat_{i}": item for i, item in enumerate(framework_data)}
    elif isinstance(framework_data, dict):
        categories = framework_data.get("governing_functions", framework_data)
    else:
        print(f"❌ Error: Unexpected data type passed to engine: {type(framework_data)}")
        db.close()
        return

    try:
        # Open transaction session container loop
        for category_key, category_content in categories.items():
            if not isinstance(category_content, dict):
                continue

            # Run validation step on standard fields
            try:
                validated_cat = Category(**category_content)
            except ValidationError as e:
                print(f"❌ Validation failed for category component {category_key}: {e.json()}")
                continue 

            # Upsert Category execution tracking rules
            db.execute(
                text("""
                    INSERT INTO compliance_categories (category_id, display_name, weight, tenant_id)
                    VALUES (:category_id, :display_name, :weight, :tenant_id)
                    ON CONFLICT (category_id, tenant_id) DO UPDATE SET
                        display_name = EXCLUDED.display_name,
                        weight = EXCLUDED.weight;
                """),
                {
                    "category_id": category_key, 
                    "display_name": validated_cat.title, 
                    "weight": validated_cat.weight, 
                    "tenant_id": tenant_id
                }
            )
            
            # Upsert Principles validation loop processing logic
            principles = category_content.get("principles", [])
            if isinstance(principles, list):
                for principle in principles:
                    if not isinstance(principle, dict): 
                        continue
                    p_id = principle.get("principle_id")
                    if not p_id: 
                        continue
                    
                    db.execute(
                        text("""
                            INSERT INTO compliance_principles (principle_id, category_id, title, description, tenant_id)
                            VALUES (:principle_id, :category_id, :title, :description, :tenant_id)
                            ON CONFLICT (principle_id, tenant_id) DO UPDATE SET
                                title = EXCLUDED.title, description = EXCLUDED.description;
                        """),
                        {
                            "principle_id": p_id, 
                            "category_id": category_key, 
                            "title": principle.get("title", "No Title"), 
                            "description": principle.get("description", ""), 
                            "tenant_id": tenant_id
                        }
                    )
                    
                    # Upsert operational verification Gates check blocks
                    gates = principle.get("checkpoints_or_gates", [])
                    if isinstance(gates, list):
                        for index, gate in enumerate(gates):
                            if not isinstance(gate, dict): 
                                continue
                            gate_id = f"GATE-{p_id}-{str(index + 1).zfill(2)}"
                            db.execute(
                                text("""
                                    INSERT INTO room_gates (gate_id, principle_id, requirement_text, validation_type, order_index, tenant_id)
                                    VALUES (:gate_id, :principle_id, :requirement_text, :validation_type, :order_index, :tenant_id)
                                    ON CONFLICT (gate_id, tenant_id) DO UPDATE SET
                                        requirement_text = EXCLUDED.requirement_text;
                                """),
                                {
                                    "gate_id": gate_id, 
                                    "principle_id": p_id, 
                                    "requirement_text": gate.get("requirement", "No Requirement"), 
                                    "validation_type": gate.get("type", "automated"), 
                                    "order_index": index, 
                                    "tenant_id": tenant_id
                                }
                            )
        db.commit()
        print("✅ Ingestion successfully completed and committed to database ledger.")
    except Exception as e:
        db.rollback()
        print(f"❌ System failure during database persistence layer execution: {str(e)}")
    finally:
        db.close()

def validate_raw_stream_data(raw_data_list: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Audits a checklist stream list against strict Pydantic rules without raising fatal exceptions.
    """
    validated_data = []
    errors = []

    for item in raw_data_list:
        try:
            record = FrameworkRequirement(**item)
            validated_data.append(record.dict())
        except ValidationError as e:
            errors.append({"item": item.get('id', 'unknown'), "error": e.json()})
            print(f"Validation failed for {item.get('id')}: {e}")
            
    return validated_data, errors

# ==========================================
# 4. TESTING ARCHITECTURE DEPLOYMENT WRAPPER
# ==========================================

if __name__ == "__main__":
    # Run the UNICEF local file configuration process tracker
    ingest_unicef_safeguarding_framework()
    
    # Create an inline sample configuration object to verify King V validation routine
    mock_framework_payload = {
        "governing_functions": {
            "CAT-01": {
                "title": "Ethical Leadership Framework",
                "weight": 1.2,
                "principles": [
                    {
                        "principle_id": "PRIN-01",
                        "title": "Integrity Controls",
                        "description": "Enforce anti-bribery tracking vectors",
                        "checkpoints_or_gates": [
                            {"requirement": "Verify automated procurement checks are active", "type": "automated"}
                        ]
                    }
                ]
            }
        }
    }
    
    print(f"DEBUG: Before calling function, data type is {type(mock_framework_payload)}")
    ingest_king_v_framework(framework_data=mock_framework_payload, tenant_id="DEMO_TENANT")
