import unittest
import os
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.room_gates.models import Base, GateEvaluation
from app.room_gates.gates_logic import RoomEngine
from app.middleware.tier_guard import TenantProfile, TierGuard

# Baseline check mock dataset matching your production king_v_checklist.json structures
MOCK_KING_V_CHECKLIST = {
    "framework_name": "King V (SADC Consolidated)",
    "governing_functions": {
        "steering_direction": {
            "title": "Steering & Setting Direction",
            "weight": 1.0,
            "principles": [
                {
                    "principle_id": "P1",
                    "title": "Ethical Board Leadership",
                    "description": "Establish long-term ethical values.",
                    "checkpoints_or_gates": [
                        {"requirement": "Verify Board Charter active signatures.", "type": "manual_upload"}
                    ]
                }
            ]
        },
        "accountability": {
            "title": "Accountability & Disclosure",
            "weight": 1.0,
            "principles": [
                {
                    "principle_id": "P12",
                    "title": "Vendor Sanction Vetting",
                    "description": "Cross-reference vendor list queries.",
                    "checkpoints_or_gates": [
                        {"requirement": "Confirm automated screening logs exist.", "type": "automated"}
                    ]
                }
            ]
        }
    }
}

class TestEthicalEdgeGRCEngine(unittest.TestCase):
    
    def setUp(self):
        """
        Creates an isolated SQLite connection pool in-memory, compiling
        the exact relational schema models declared inside the package.
        """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = self.SessionLocal()
        
        # Manually create tables not directly managed by SQLAlchemy declarative models
        # (Matches tables defined in Section 11, 12, and 13 of init_schema.sql)
        self.db.execute(text("""
            CREATE TABLE IF NOT EXISTS compliance_categories (
                category_id VARCHAR(100) PRIMARY KEY,
                display_name VARCHAR(255) NOT NULL,
                weight REAL DEFAULT 1.0
            );
        """))
        self.db.execute(text("""
            CREATE TABLE IF NOT EXISTS compliance_principles (
                principle_id VARCHAR(50) PRIMARY KEY,
                category_id VARCHAR(100) NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT
            );
        """))
        self.db.execute(text("""
            CREATE TABLE IF NOT EXISTS room_gates (
                gate_id VARCHAR(50) PRIMARY KEY,
                principle_id VARCHAR(50) NOT NULL,
                requirement_text TEXT NOT NULL,
                validation_type VARCHAR(50) DEFAULT 'automated',
                order_index INTEGER DEFAULT 0
            );
        """))
        self.db.commit()

    def tearDown(self):
        """Safely tears down the test database connection."""
        self.db.close()
        Base.metadata.drop_all(self.engine)

    def test_framework_ingestion_pipeline(self):
        """
        Tests parsing of King V structural configurations and verifies 
        relational constraints inside the master framework tables.
        """
        # Execute map-injection mock routine
        categories = MOCK_KING_V_CHECKLIST["governing_functions"]
        for cat_id, cat_content in categories.items():
            self.db.execute(
                text("INSERT INTO compliance_categories (category_id, display_name, weight) VALUES (:id, :name, :w)"),
                {"id": cat_id, "name": cat_content["title"], "w": cat_content.get("weight", 1.0)}
            )
            for p in cat_content["principles"]:
                self.db.execute(
                    text("INSERT INTO compliance_principles (principle_id, category_id, title, description) VALUES (:id, :cat, :t, :d)"),
                    {"id": p["principle_id"], "cat": cat_id, "t": p["title"], "d": p["description"]}
                )
                for idx, gate in enumerate(p["checkpoints_or_gates"]):
                    self.db.execute(
                        text("INSERT INTO room_gates (gate_id, principle_id, requirement_text, validation_type, order_index) VALUES (:gid, :pid, :r, :v, :idx)"),
                        {
                            "gid": f"GATE-{p['principle_id']}-{str(idx + 1).zfill(2)}",
                            "pid": p["principle_id"],
                            "r": gate["requirement"],
                            "v": gate["type"],
                            "idx": idx
                        }
                    )
        self.db.commit()

        # Query and assert ingestion results
        total_principles = self.db.execute(text("SELECT COUNT(*) FROM compliance_principles;")).scalar()
        total_gates = self.db.execute(text("SELECT COUNT(*) FROM room_gates;")).scalar()
        
        self.assertEqual(total_principles, 2, "Framework principles ingestion mismatch.")
        self.assertEqual(total_gates, 2, "Framework compliance gates ingestion mismatch.")

    def test_room_engine_mathematical_scoring(self):
        """
        Populates mock data and asserts that RoomEngine's SQL queries
        properly execute compliance scoring without throwing division anomalies.
        """
        # Set up framework checkpoints in the isolated database
        self.db.execute(text("INSERT INTO room_gates (gate_id, principle_id, requirement_text) VALUES ('GATE-P1-01', 'P1', 'Req 1');"))
        self.db.execute(text("INSERT INTO room_gates (gate_id, principle_id, requirement_text) VALUES ('GATE-P1-02', 'P1', 'Req 2');"))
        self.db.commit()

        # Instantiate RoomEngine and compute scoring metrics before compliance evaluations
        engine = RoomEngine(self.db)
        initial_matrix = engine.calculate_active_room_scores()
        
        # Verify initial states reflect 0% (0 gates passed out of 2 total)
        self.assertEqual(initial_matrix["P1"]["passed"], 0)
        self.assertEqual(initial_matrix["P1"]["total"], 2)

        # Evaluate and pass one gate: GATE-P1-01 (Updates gate_evaluations Table)
        engine.evaluate_single_gate_telemetry(
            assessment_id="11111111-1111-1111-1111-111111111111",
            gate_id="GATE-P1-01",
            check_passed=True,
            telemetry_url="/proof/file.txt"
        )

        # Recalculate scoring metrics
        updated_matrix = engine.calculate_active_room_scores()
        self.assertEqual(updated_matrix["P1"]["passed"], 1)
        self.assertEqual(updated_matrix["P1"]["total"], 2)

    def test_tier_guard_bandwidth_restrictions(self):
        """
        Ensures that TierGuard enforces file size boundaries and raises
        correct, user-friendly HTTP errors depending on client tier scopes.
        """
        # 1. Verify Professional Tier throws HTTP 429 when exceeding limits
        prof_tenant = TenantProfile(token="key_prof", name="SaaS Corp", tier="Professional", current_usage_mb=245)
        
        with self.assertRaises(Exception) as context:
            TierGuard.enforce_upload_limits(prof_tenant, incoming_payload_size_mb=10.5) # Exceeds 250MB limit
            
        self.assertIn("Subscription Upload Cap Exceeded", str(context.exception))

        # 2. Verify Standard Tier limits uploads remotely to protect cloud margins
        standard_tenant = TenantProfile(token="key_std", name="SME Local", tier="Standard", current_usage_mb=0)
        
        with self.assertRaises(Exception) as context:
            TierGuard.enforce_upload_limits(standard_tenant, incoming_payload_size_mb=6.0) # Exceeds 5MB cloud limit
            
        self.assertIn("Standard Core Cloud instances are limited to 5MB", str(context.exception))

if __name__ == "__main__":
    print("🚦 Launching Ethical Edge Local Integration Test Suite...")
    unittest.main()
