from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
async def get_auth():
    return "{'Hello', 'world'}"