#!/bin/bash
echo "======================================================================"
echo "🚀 STARTING ETHICAL EDGE OPEN GRC ENGINE AUTOMATED ENVIRONMENT 🚀"
echo "======================================================================"

# Step 1: Stop any old stray containers running in the background
echo "-> Cleaning up historical container states..."
docker-compose down -v

# Step 2: Build and launch the network architecture
echo "-> Compiling application images and starting services..."
docker-compose up --build -d

echo "-> Waiting for database container initialization (5 seconds)..."
sleep 5

# Step 3: Execute your end-to-end multi-room verification suite inside the live container
echo "-> Running comprehensive multi-room integration tests..."
docker-compose exec web python test_multi_room.py

echo "======================================================================"
echo "✨ SYSTEM IS ONLINE! Interactive Swagger API Docs live at:"
echo "👉 http://localhost:8000/docs"
echo "======================================================================"
