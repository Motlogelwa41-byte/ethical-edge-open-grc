import os
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column, String, TEXT, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Session
from pgvector.sqlalchemy import Vector
from openai import OpenAI

# 1. SETUP THE ROUTER
router = APIRouter(prefix="/api/v1/ai-automation", tags=["CertiGuard AI Agent"])

# 2. SETUP OPENAI CLIENT (Ensure OPENAI_API_KEY is in your environment variables)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 3. INITIALIZE TABLES ON STARTUP (Runs raw SQL automatically to prevent setup headaches)
def init_vector_db_tables(db: Session):
    """Executes the strict multi-tenant database setup directly."""
    db.execute(text("CREATE EXTENSION IF NOT EXISTS pgvector;"))
    
    db.execute(text("""
    CREATE TABLE IF NOT EXISTS qna_vector_embeddings (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        tenant_id UUID NOT NULL,
        input_text TEXT NOT NULL,
        output_text TEXT NOT NULL,
        metadata JSONB DEFAULT '{}'::jsonb,
        embedding vector(1536),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """))
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_v_tenant ON qna_vector_embeddings(tenant_id);"))
    db.commit()

# 4. UTILITY TO GENERATE EMBEDDINGS
def get_embedding(text_string: str) -> list[float]:
    clean_text = text_string.replace("\n", " ")
    response = openai_client.embeddings.create(
        input=[clean_text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# 5. THE SECURE, MULTI-TENANT SEARCH ENDPOINT
# Replace 'get_db' and 'get_current_tenant_id' with your actual dependency imports
from app.database import get_db 
from app.auth.dependencies import get_current_tenant_id 

@router.post("/process-question")
async def process_questionnaire_item(
    question: str, 
    db: Session = Depends(get_db), 
    tenant_id: str = Depends(get_current_tenant_id)
):
    # Ensure tables are built smoothly
    init_vector_db_tables(db)
    
    # Generate mathematical vector for the incoming question
    try:
        vector_representation = get_embedding(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Service Failure: {str(e)}")

    # Execute strict tenant-isolated vector match
    query = text("""
        SELECT input_text, output_text, (1 - (embedding <=> :vector::vector)) AS similarity
        FROM qna_vector_embeddings
        WHERE tenant_id = :tenant_id
        ORDER BY embedding <=> :vector::vector
        LIMIT 1;
    """)
    
    match = db.execute(
        query, 
        {"vector": str(vector_representation), "tenant_id": tenant_id}
    ).fetchone()

    # If confidence score is below 70%, refuse to give a bad answer
    if not match or match.similarity < 0.70:
        return {
            "status": "Review Required",
            "suggested_answer": "No confident match found in your tenant database policy files.",
            "confidence": 0.0
        }

    return {
        "status": "Auto-Drafted",
        "matched_policy_context": match.input_text,
        "suggested_answer": match.output_text,
        "confidence": round(float(match.similarity), 3)
    }
