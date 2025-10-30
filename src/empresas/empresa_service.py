from sqlalchemy.orm import Session
from typing import List, Optional
from .entity.empresa_entity import Empresa
from ..auth.entity.user_entity import User
import hashlib
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
        stellar_public_key, _ = StellarKeyGenerator.generate_keypair_from_empresa_data(
            rfc=empresa_data.rfc,
            email=empresa_data.email,
            nombre=empresa_data.nombre
        )
        
        # Crear empresa con claves Stellar generadas (sin incluir password en la entidad Empresa)
        empresa_dict = empresa_data.dict(exclude={"password"})
        empresa_dict['stellar_public_key'] = stellar_public_key
        empresa_dict['stellar_secret_key'] = _
        
        empresa = self.repository.create_from_dict(empresa_dict)

        # Crear usuario asociado (simple): email de la empresa, nombre fijo "empresa"
        # Si ya existe, no crear de nuevo
        existing_user = self.repository.db.query(User).filter(User.email == empresa_data.email.lower()).first()
        if not existing_user:
            password_hash = hashlib.sha256(empresa_data.password.encode('utf-8')).hexdigest()
            user = User(
                email=empresa_data.email.lower(),
                password_hash=password_hash,
                name="empresa",
                status="active",
            )
            self.repository.db.add(user)
            self.repository.db.commit()
            self.repository.db.refresh(user)
            # Generar y asignar claves Stellar para el usuario creado
            user_pub, user_sec = StellarKeyGenerator.generate_keypair_from_user_data(
                email=user.email,
                nombre="empresa",
                apellido=""
            )
            user.stellar_public_key = user_pub
            user.stellar_secret_key = user_sec
            self.repository.db.commit()
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
