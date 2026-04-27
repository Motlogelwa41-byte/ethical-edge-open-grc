cat <<EOF > app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initializes the database by creating all tables defined in models.py
    """
    from . import models
    print("Connecting to engine and creating tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def save_automated_risk(db_session, risk_data):
    from . import models
    from .risk import RiskEngine
    
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
EOF
