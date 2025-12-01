from fastapi import APIRouter
from typing import Dict

router = APIRouter(prefix='/health')


@router.get('')
async def health() -> Dict[str, str]:
    return {'status': 'ok'}
