from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.embedding import get_text_embedding
# Import your authentication layer that delivers tenant context
from app.auth.dependencies import get_current_tenant_id 

router = APIRouter(prefix="/questionnaire", tags=["AI Questionnaire Automation"])

@router.post("/ask-agent")
async def ask_ai_agent(
    question: str, 
    db: Session = Depends(get_db), 
    tenant_id: str = Depends(get_current_tenant_id)
):
    # 1. Convert incoming question from spreadsheet into a vector
    try:
        question_vector = get_text_embedding(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")

    # 2. Run multi-tenant semantic search via raw SQL / Cosine Distance (<=>)
    query = """
        SELECT input_text, output_text, (1 - (embedding <=> :vector::vector)) AS similarity
        FROM qna_vector_embeddings
        WHERE tenant_id = :tenant_id
        ORDER BY embedding <=> :vector::vector
        LIMIT 1;
    """
    
    result = db.execute(
        query, 
        {"vector": str(question_vector), "tenant_id": tenant_id}
    ).fetchone()

    if not result or result.similarity < 0.70:
        return {
            "question": question,
            "suggested_answer": "No highly confident matching framework policies found. Please review manually.",
            "confidence_score": 0.0
        }

    return {
        "question": question,
        "matched_context": result.input_text,
        "suggested_answer": result.output_text,
        "confidence_score": round(float(result.similarity), 3)
    }
