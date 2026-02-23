from fastapi import APIRouter

from typing import Optional


file_router = APIRouter()

@file_router.get("/file")
def get_file(id: Optional[int], path: Optional[str]):
    return {}
    
