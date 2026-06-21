import uuid
from sqlalchemy import Column, String, TEXT, ForeignKey, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from pgvector.sqlalchemy import Vector
from app.database import Base

class QnaKnowledgeSource(Base):
    __tablename__ = "qna_knowledge_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    source_type = Column(String(50), nullable=False) # 'POLICY', 'RISK_CONTROL'
    source_name = Column(String(255), nullable=False)
    file_path = Column(TEXT, nullable=True)

class QnaVectorEmbedding(Base):
    __tablename__ = "qna_vector_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("qna_knowledge_sources.id", ondelete="CASCADE"))
    input_text = Column(TEXT, nullable=False)
    output_text = Column(TEXT, nullable=False)
    metadata = Column(JSONB, default={})
    embedding = Column(Vector(1536)) # Fixed dimension for standard OpenAI text-embedding-3-small
