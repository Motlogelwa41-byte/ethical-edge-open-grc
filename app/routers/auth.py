from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

print("AUTH ROUTER FILE LOADED")

@router.get("/ping")
def ping():
    return {"status": "auth is loading"}
