from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from .entity.token_entity import TokenCO2
from .dto.token_dto import TokenCreateDTO, TokenUpdateDTO


class TokenRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, token_data: TokenCreateDTO) -> TokenCO2:
        token = TokenCO2(**token_data.dict())
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token
    
    def get_by_id(self, token_id: int) -> Optional[TokenCO2]:
        return self.db.query(TokenCO2).filter(TokenCO2.token_id == token_id).first()
    
    def get_available(self, skip: int = 0, limit: int = 100) -> List[TokenCO2]:
        return self.db.query(TokenCO2).filter(
            TokenCO2.status == "disponible"
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[TokenCO2]:
        return self.db.query(TokenCO2).filter(
            TokenCO2.status == status
        ).offset(skip).limit(limit).all()
    
    def update_status(self, token_id: int, status: str) -> Optional[TokenCO2]:
        token = self.get_by_id(token_id)
        if not token:
            return None
        
        token.status = status
        self.db.commit()
        self.db.refresh(token)
        return token
    
    def reserve_tokens(self, token_ids: List[int]) -> List[TokenCO2]:
        tokens = self.db.query(TokenCO2).filter(
            and_(
                TokenCO2.token_id.in_(token_ids),
                TokenCO2.status == "disponible"
            )
        ).all()
        
        for token in tokens:
            token.status = "reservado"
        
        self.db.commit()
        return tokens
    
    def release_tokens(self, token_ids: List[int]) -> List[TokenCO2]:
        tokens = self.db.query(TokenCO2).filter(
            and_(
                TokenCO2.token_id.in_(token_ids),
                TokenCO2.status == "reservado"
            )
        ).all()
        
        for token in tokens:
            token.status = "disponible"
        
        self.db.commit()
        return tokens
    
    def sell_tokens(self, token_ids: List[int]) -> List[TokenCO2]:
        tokens = self.db.query(TokenCO2).filter(
            and_(
                TokenCO2.token_id.in_(token_ids),
                TokenCO2.status == "reservado"
            )
        ).all()
        
        for token in tokens:
            token.status = "vendido"
        
        self.db.commit()
        return tokens
    
    def count_by_status(self, status: str) -> int:
        return self.db.query(TokenCO2).filter(TokenCO2.status == status).count()
    
    def get_total_co2_available(self) -> float:
        result = self.db.query(TokenCO2.cantidad_co2).filter(
            TokenCO2.status == "disponible"
        ).all()
        return sum([float(row[0]) for row in result])
