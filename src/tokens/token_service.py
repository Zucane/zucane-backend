from sqlalchemy.orm import Session
from typing import List, Optional
from .entity.token_entity import TokenCO2
from .dto.token_dto import TokenCreateDTO, TokenUpdateDTO, TokenResponseDTO, TokenListDTO, TokenReservaDTO
from .token_repository import TokenRepository


class TokenService:
    
    def __init__(self, db: Session):
        self.repository = TokenRepository(db)
    
    def emitir_token(self, token_data: TokenCreateDTO) -> TokenResponseDTO:
        token = self.repository.create(token_data)
        return TokenResponseDTO.from_orm(token)
    
    def obtener_token(self, token_id: int) -> Optional[TokenResponseDTO]:
        token = self.repository.get_by_id(token_id)
        if not token:
            return None
        return TokenResponseDTO.from_orm(token)
    
    def listar_tokens_disponibles(self, page: int = 1, size: int = 10) -> TokenListDTO:
        skip = (page - 1) * size
        tokens = self.repository.get_available(skip=skip, limit=size)
        total = self.repository.count_by_status("disponible")
        
        tokens_dto = [TokenResponseDTO.from_orm(token) for token in tokens]
        
        return TokenListDTO(
            tokens=tokens_dto,
            total=total,
            page=page,
            size=size
        )
    
    def listar_tokens_por_status(self, status: str, page: int = 1, size: int = 10) -> TokenListDTO:
        skip = (page - 1) * size
        tokens = self.repository.get_by_status(status, skip=skip, limit=size)
        total = self.repository.count_by_status(status)
        
        tokens_dto = [TokenResponseDTO.from_orm(token) for token in tokens]
        
        return TokenListDTO(
            tokens=tokens_dto,
            total=total,
            page=page,
            size=size
        )
    
    def reservar_tokens(self, reserva_data: TokenReservaDTO) -> List[TokenResponseDTO]:
        tokens = self.repository.reserve_tokens(reserva_data.token_ids)
        
        if len(tokens) != len(reserva_data.token_ids):
            # Liberar tokens reservados si no se pudieron reservar todos
            self.repository.release_tokens([t.token_id for t in tokens])
            raise ValueError("No todos los tokens están disponibles")
        
        return [TokenResponseDTO.from_orm(token) for token in tokens]
    
    def liberar_tokens(self, token_ids: List[int]) -> List[TokenResponseDTO]:
        tokens = self.repository.release_tokens(token_ids)
        return [TokenResponseDTO.from_orm(token) for token in tokens]
    
    def vender_tokens(self, token_ids: List[int]) -> List[TokenResponseDTO]:
        tokens = self.repository.sell_tokens(token_ids)
        return [TokenResponseDTO.from_orm(token) for token in tokens]
    
    def obtener_inventario(self) -> dict:
        return {
            "disponibles": self.repository.count_by_status("disponible"),
            "reservados": self.repository.count_by_status("reservado"),
            "vendidos": self.repository.count_by_status("vendido"),
            "total_co2_disponible": self.repository.get_total_co2_available()
        }
