from fastapi import APIRouter

from app.api.api_v2.endpoints import domain, health, meta, record, rtype, ttl, user

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(meta.router, prefix="/meta", tags=["meta"])
api_router.include_router(ttl.router, prefix="/ttls", tags=["ttls"])
api_router.include_router(rtype.router, prefix="/rtypes", tags=["rtypes"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(record.router, prefix="/records", tags=["records"])
api_router.include_router(domain.router, prefix="/domains", tags=["domains"])
