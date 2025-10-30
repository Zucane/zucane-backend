from fastapi import Request, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
from .database import get_db
from ..system.entity.idempotency_key_entity import IdempotencyKey
from datetime import datetime, timedelta
import json


class IdempotencyService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_idempotency_key(self, key: str) -> Optional[IdempotencyKey]:
        return self.db.query(IdempotencyKey).filter(
            IdempotencyKey.key == key,
            IdempotencyKey.expires_at > datetime.utcnow()
        ).first()
    
    def create_idempotency_key(self, key: str, scope: str, response_json: str = None) -> IdempotencyKey:
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        idempotency_key = IdempotencyKey(
            key=key,
            scope=scope,
            response_json=response_json,
            expires_at=expires_at
        )
        
        self.db.add(idempotency_key)
        self.db.commit()
        self.db.refresh(idempotency_key)
        
        return idempotency_key
    
    def update_response(self, key: str, response_json: str):
        idempotency_key = self.get_idempotency_key(key)
        if idempotency_key:
            idempotency_key.response_json = response_json
            self.db.commit()


def get_idempotency_key(request: Request) -> Optional[str]:
    return request.headers.get("Idempotency-Key")


def check_idempotency(
    idempotency_key: Optional[str] = Depends(get_idempotency_key),
    db: Session = Depends(get_db)
):
    if not idempotency_key:
        return None
    
    service = IdempotencyService(db)
    existing_key = service.get_idempotency_key(idempotency_key)
    
    if existing_key and existing_key.response_json:
        response_data = json.loads(existing_key.response_json)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Operación ya procesada",
            headers={"X-Idempotency-Key": idempotency_key}
        )
    
    return idempotency_key
