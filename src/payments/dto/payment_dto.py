#!/usr/bin/env python3
"""
DTOs para pagos con Stellar
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class PaymentRequestDTO(BaseModel):
    """DTO para solicitar pago en Stellar"""
    transaccion_id: int
    empresa_secret_key: Optional[str] = None  # Opcional para testing
    
class PaymentResponseDTO(BaseModel):
    """DTO para respuesta de pago"""
    success: bool
    transaction_hash: Optional[str] = None
    ledger: Optional[int] = None
    created_at: Optional[str] = None
    fee_charged: Optional[str] = None
    error: Optional[str] = None
    amount: Optional[float] = None
    token_id: Optional[int] = None

class PaymentVerificationDTO(BaseModel):
    """DTO para verificar pago"""
    transaction_hash: str

class PaymentVerificationResponseDTO(BaseModel):
    """DTO para respuesta de verificación"""
    success: bool
    verified: Optional[bool] = None
    hash: Optional[str] = None
    ledger: Optional[int] = None
    created_at: Optional[str] = None
    operations: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

class BalanceRequestDTO(BaseModel):
    """DTO para consultar balance"""
    empresa_id: int

class BalanceResponseDTO(BaseModel):
    """DTO para respuesta de balance"""
    success: bool
    xochi_balance: Optional[float] = None
    xlm_balance: Optional[float] = None
    account_exists: Optional[bool] = None
    account_info: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class StellarTransactionDTO(BaseModel):
    """DTO para transacción Stellar"""
    transaction_hash: str
    ledger: int
    created_at: str
    successful: bool
    fee_charged: str
    operations: List[Dict[str, Any]]
    
class StellarAccountDTO(BaseModel):
    """DTO para cuenta Stellar"""
    account_id: str
    balances: List[Dict[str, Any]]
    sequence: str
    subentry_count: int
