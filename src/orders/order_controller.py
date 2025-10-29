from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..shared.database import get_db
from ..shared.auth import require_company_user
from .dto.order_dto import OrderCreateDTO, OrderResponseDTO, OrderListDTO

router = APIRouter(prefix="/orders", tags=["reservas"])


@router.post("/", response_model=OrderResponseDTO, status_code=201)
async def crear_orden(
    order_data: OrderCreateDTO,
    db: Session = Depends(get_db),
    current_user = Depends(require_company_user)
):
    
    raise HTTPException(
        status_code=501, 
        detail="Endpoint en desarrollo"
    )


@router.get("/", response_model=OrderListDTO)
async def listar_ordenes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(require_company_user)
):
    
    raise HTTPException(
        status_code=501, 
        detail="Endpoint en desarrollo"
    )


@router.get("/{order_id}", response_model=OrderResponseDTO)
async def obtener_orden(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_company_user)
):
    
    raise HTTPException(
        status_code=501, 
        detail="Endpoint en desarrollo"
    )


@router.post("/{order_id}/expire")
async def expirar_orden(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_company_user)
):
    
    raise HTTPException(
        status_code=501, 
        detail="Endpoint en desarrollo"
    )
