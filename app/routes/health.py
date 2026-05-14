from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.get("/readiness")
def readiness():
    return {
        "status": "ready"
    }