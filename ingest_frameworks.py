def ingest_king_v_framework(data, db, tenant_id):
    # 1. VALIDATION STAGE
    # Use Pydantic to parse/clean the entire tree before touching the DB
    try:
        # Assuming you defined a 'FrameworkRoot' model that nests Principles
        # and Principles nest Gates
        validated_data = FrameworkRoot(data=data) 
    except ValidationError as e:
        print(f"❌ Critical Validation Error: {e.json()}")
        return # Do not proceed to DB if schema is broken

    # 2. ITERATE AND VALIDATE
    for category_key, category_content in categories.items():
        if not isinstance(category_content, dict):
            continue

        # VALIDATION STAGE
        try:
            validated_cat = Category(**category_content)
        except ValidationError as e:
            # --- PASTE THIS HERE ---
            error_msg = f"Validation failed for {category_key}: {e.json()}"
            print(f"❌ {error_msg}")
            
            # If you have a logging function or a file write, put it here
            # e.g., self.log_to_audit(error_msg)
            
            continue # This ensures the loop continues to the next category
        
        # ... rest of your code ...

    # 2. PERSISTENCE STAGE
    with db.session() as session:
        # Now iterate through the validated objects
        for category in validated_data.categories:
            # Upsert Category ...
            # Upsert Principles ...
            # Upsert Gates ...
            session.commit()
            print("✅ Ingestion successfully completed!")

print(f"DEBUG: Before calling function, data type is {type(data)}")
ingest_king_v_framework(data, db, tenant_id)
   # Replace the block that checks for TARGET_TENANT_ID with this:
tenant_id = "DEMO_TENANT" 
# tenant_id = os.getenv("TARGET_TENANT_ID")  <-- Comment out or delete this
    # STANDARDIZE: If it's a list, we wrap it into a dictionary structure
    if isinstance(framework_data, list):
        # We assume the list is a sequence of category dictionaries
        categories = {f"cat_{i}": item for i, item in enumerate(framework_data)}
    elif isinstance(framework_data, dict):
        categories = framework_data.get("governing_functions", framework_data)
    else:
        print(f"❌ Error: Unexpected data type: {type(framework_data)}")
        return

    # ITERATE
    for category_key, category_content in categories.items():
        # SAFETY CHECK: Only process if category_content is a dict
        if not isinstance(category_content, dict):
            continue

        # Upsert Category
        session.execute(
            text("""
                INSERT INTO compliance_categories (category_id, display_name, weight, tenant_id)
                VALUES (:category_id, :display_name, :weight, :tenant_id)
                ON CONFLICT (category_id, tenant_id) DO UPDATE SET
                    display_name = EXCLUDED.display_name,
                    weight = EXCLUDED.weight;
            """),
            {
                "category_id": category_key, 
                "display_name": category_content.get("title", "Unknown"), 
                "weight": category_content.get("weight", 1.0), 
                "tenant_id": tenant_id
            }
        )
        
        # Upsert Principles
        principles = category_content.get("principles", [])
        if isinstance(principles, list):
            for principle in principles:
                if not isinstance(principle, dict): continue
                p_id = principle.get("principle_id")
                if not p_id: continue
                
                session.execute(
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
                
                # Upsert Gates
                gates = principle.get("checkpoints_or_gates", [])
                if isinstance(gates, list):
                    for index, gate in enumerate(gates):
                        if not isinstance(gate, dict): continue
                        gate_id = f"GATE-{p_id}-{str(index + 1).zfill(2)}"
                        session.execute(
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
    session.commit()
    print("✅ Ingestion successfully completed!")

from pydantic import ValidationError
from .schemas import FrameworkRequirement

def ingest_data(raw_data_list):
    validated_data = []
    errors = []

    for item in raw_data_list:
        try:
            # This attempts to map and validate the data
            record = FrameworkRequirement(**item)
            validated_data.append(record.dict())
        except ValidationError as e:
            # Log the specific issue without crashing the whole process
            errors.append({"item": item.get('id'), "error": e.json()})
            print(f"Validation failed for {item.get('id')}: {e}")
    
    return validated_data, errors
