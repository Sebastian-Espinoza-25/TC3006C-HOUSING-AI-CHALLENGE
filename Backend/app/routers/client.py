from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health():
    return {"message": "This end point is working."}
