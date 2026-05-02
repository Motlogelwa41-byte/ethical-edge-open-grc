from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/test")
def test():
    return {"status": "auth router working"}
