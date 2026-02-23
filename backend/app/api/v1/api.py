from fastapi import APIRouter

from .routes import shortlink, qrcode, search, tmpfile, blob

router = APIRouter()

router.include_router(shortlink.router)
router.include_router(qrcode.router)
router.include_router(search.router)
router.include_router(tmpfile.router)
router.include_router(blob.router)
