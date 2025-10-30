from sqlalchemy.orm import Session
from typing import List, Optional
from .entity.empresa_entity import Empresa
from .dto.empresa_dto import EmpresaCreateDTO, EmpresaUpdateDTO, EmpresaResponseDTO, EmpresaListDTO
from .empresa_repository import EmpresaRepository
from ..stellar.key_generator import StellarKeyGenerator


class EmpresaService:
    
    def __init__(self, db: Session):
        self.repository = EmpresaRepository(db)
    
    def crear_empresa(self, empresa_data: EmpresaCreateDTO) -> EmpresaResponseDTO:
        # Validar que el RFC no exista
        if self.repository.get_by_rfc(empresa_data.rfc):
            raise ValueError("Ya existe una empresa con este RFC")
        
        # Generar claves Stellar determinísticas
        stellar_public_key, stellar_secret_key = StellarKeyGenerator.generate_keypair_from_empresa_data(
            rfc=empresa_data.rfc,
            email=empresa_data.email,
            nombre=empresa_data.nombre
        )
        
        # Crear empresa con claves Stellar generadas
        empresa_dict = empresa_data.dict()
        empresa_dict['stellar_public_key'] = stellar_public_key
        empresa_dict['stellar_secret_key'] = stellar_secret_key  # Guardar también la secret key
        
        empresa = self.repository.create_from_dict(empresa_dict)
        return EmpresaResponseDTO.model_validate(empresa)
    
    def obtener_empresa(self, empresa_id: int) -> Optional[EmpresaResponseDTO]:
        empresa = self.repository.get_by_id(empresa_id)
        if not empresa:
            return None
        return EmpresaResponseDTO.model_validate(empresa)
    
    def obtener_empresa_por_rfc(self, rfc: str) -> Optional[EmpresaResponseDTO]:
        empresa = self.repository.get_by_rfc(rfc)
        if not empresa:
            return None
        return EmpresaResponseDTO.model_validate(empresa)
    
    def listar_empresas(self, page: int = 1, size: int = 10, status: str = "activo") -> EmpresaListDTO:
        skip = (page - 1) * size
        empresas = self.repository.get_all(skip=skip, limit=size, status=status)
        total = self.repository.count(status=status)
        
        empresas_dto = [EmpresaResponseDTO.model_validate(empresa) for empresa in empresas]
        
        return EmpresaListDTO(
            empresas=empresas_dto,
            total=total,
            page=page,
            size=size
        )
    
    def actualizar_empresa(self, empresa_id: int, empresa_data: EmpresaUpdateDTO) -> Optional[EmpresaResponseDTO]:
        empresa = self.repository.update(empresa_id, empresa_data)
        if not empresa:
            return None
        return EmpresaResponseDTO.model_validate(empresa)
    
    def desactivar_empresa(self, empresa_id: int) -> Optional[EmpresaResponseDTO]:
        empresa = self.repository.get_by_id(empresa_id)
        if not empresa:
            return None
        
        empresa.status = "inactivo"
        self.repository.db.commit()
        self.repository.db.refresh(empresa)
        return EmpresaResponseDTO.model_validate(empresa)
    
    def activar_empresa(self, empresa_id: int) -> Optional[EmpresaResponseDTO]:
        empresa = self.repository.get_by_id(empresa_id)
        if not empresa:
            return None
        
        empresa.status = "activo"
        self.repository.db.commit()
        self.repository.db.refresh(empresa)
        return EmpresaResponseDTO.model_validate(empresa)
    
    def validar_empresa_activa(self, empresa_id: int) -> bool:
        empresa = self.repository.get_by_id(empresa_id)
        return empresa and empresa.status == "activo"
