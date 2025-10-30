from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..shared.database import get_db
from ..shared.auth import require_gov_admin
from .dto.system_dto import OutboxEventResponseDTO

router = APIRouter(prefix="/system", tags=["sistema"])


@router.get("/outbox/events", response_model=list[OutboxEventResponseDTO])
async def listar_eventos_pendientes(
    db: Session = Depends(get_db),
    current_user = Depends(require_gov_admin)
):
    
    raise HTTPException(
        status_code=501, 
        detail="Endpoint en desarrollo"
    )


@router.post("/outbox/events/{event_id}/process")
async def procesar_evento(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_gov_admin)
):

    raise HTTPException(
        status_code=501, 
        detail="Endpoint en desarrollo"
    )


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Sistema funcionando correctamente"
    }
