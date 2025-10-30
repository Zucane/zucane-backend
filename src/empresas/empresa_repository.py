from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from .entity.empresa_entity import Empresa
from .dto.empresa_dto import EmpresaCreateDTO, EmpresaUpdateDTO


class EmpresaRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, empresa_data: EmpresaCreateDTO) -> Empresa:
        empresa = Empresa(**empresa_data.dict())
        self.db.add(empresa)
        self.db.commit()
        self.db.refresh(empresa)
        return empresa
    
    def create_from_dict(self, empresa_dict: dict) -> Empresa:
        empresa = Empresa(**empresa_dict)
        self.db.add(empresa)
        self.db.commit()
        self.db.refresh(empresa)
        return empresa
    
    def get_by_id(self, empresa_id: int) -> Optional[Empresa]:
        return self.db.query(Empresa).filter(Empresa.empresa_id == empresa_id).first()
    
    def get_by_rfc(self, rfc: str) -> Optional[Empresa]:
        return self.db.query(Empresa).filter(Empresa.rfc == rfc).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, status: str = "activo") -> List[Empresa]:
        query = self.db.query(Empresa)
        if status:
            query = query.filter(Empresa.status == status)
        return query.offset(skip).limit(limit).all()
    
    def update(self, empresa_id: int, empresa_data: EmpresaUpdateDTO) -> Optional[Empresa]:
        empresa = self.get_by_id(empresa_id)
        if not empresa:
            return None
        
        update_data = empresa_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(empresa, field, value)
        
        self.db.commit()
        self.db.refresh(empresa)
        return empresa
    
    def delete(self, empresa_id: int) -> bool:
        empresa = self.get_by_id(empresa_id)
        if not empresa:
            return False
        
        empresa.status = "inactivo"
        self.db.commit()
        return True
    
    def count(self, status: str = "activo") -> int:
        query = self.db.query(Empresa)
        if status:
            query = query.filter(Empresa.status == status)
        return query.count()
