from sqlalchemy import create_all, create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from . import models

def save_automated_risk(db_session, risk_data):
    """
    Saves a risk to the database automatically when a vetting fails.
    """
    from .risk import RiskEngine # Local import to avoid circular dependencies
    
    score = RiskEngine.calculate_score(risk_data['likelihood'], risk_data['impact'])
    level = RiskEngine.get_risk_level(score)
    treatment = RiskEngine.suggest_treatment(score)
    
    new_risk = models.Risk(
        title=risk_data['title'],
        description=risk_data['description'],
        likelihood=risk_data['likelihood'],
        impact=risk_data['impact'],
        score=score,
        risk_level=level,
        treatment=treatment
    )
    
    db_session.add(new_risk)
    db_session.commit()
    db_session.refresh(new_risk)
    return new_risk
