#!/bin/bash
echo "======================================================================"
echo "🚀 STARTING ETHICAL EDGE OPEN GRC ENGINE..."
echo "======================================================================"

# 1. Clean up
docker-compose down -v

# 2. Build and launch
echo "-> Compiling and starting services..."
docker-compose up --build -d

# 3. Wait for DB to be ready
echo "-> Waiting for database..."
sleep 10

# 4. CRITICAL: Perform Data Ingestion inside the running container
echo "-> Injecting Framework Data..."
docker-compose exec -T web python3 -m ingest_frameworks

# 5. Run tests to confirm integrity
echo "-> Running integration tests..."
docker-compose exec -T web python3 test_master_pipeline.py

echo "======================================================================"
echo "✨ SYSTEM IS ONLINE! Docs: http://localhost:8000/docs"
echo "======================================================================"

#!/bin/bash
# ... (Keep your existing docker-compose up steps here)

echo "-> Running automated compliance integrity checks..."
docker-compose exec -T web python3 run_compliance_checks.py

echo "-> Triggering Audit Engine..."
docker-compose exec -T web python3 test_master_pipeline.py
