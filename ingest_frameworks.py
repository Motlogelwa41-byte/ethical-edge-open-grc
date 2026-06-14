def ingest_king_v_framework(framework_data: Any, session: Session, tenant_id: str):
    print(f"🚀 Injecting framework for Tenant: {tenant_id}")
    
    # Robust handling: If it's a list, wrap it to match the expected structure
    if isinstance(framework_data, list):
        print("ℹ️ Detected list format, wrapping into governing_functions...")
        categories = {f"cat_{i}": item for i, item in enumerate(framework_data)}
    else:
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
            {"category_id": category_key, "display_name": category_content.get("title", "Unknown"), 
             "weight": category_content.get("weight", 1.0), "tenant_id": tenant_id}
        )
        
        # 2. Upsert Principles
        for principle in category_content.get("principles", []):
            p_id = principle.get("principle_id")
            if not p_id: continue
            
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
