from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..system.entity.outbox_event_entity import OutboxEvent


class OutboxService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_event(
        self, 
        aggregate_type: str, 
        aggregate_id: int, 
        event_type: str, 
        payload: dict
    ) -> OutboxEvent:
        event = OutboxEvent(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload_json=str(payload),
            status="pending"
        )
        
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        
        return event
    
    def get_pending_events(self, limit: int = 100) -> List[OutboxEvent]:
        return self.db.query(OutboxEvent).filter(
            OutboxEvent.status == "pending"
        ).limit(limit).all()
    
    def mark_as_sent(self, event_id: int):
        event = self.db.query(OutboxEvent).filter(
            OutboxEvent.event_id == event_id
        ).first()
        
        if event:
            event.status = "sent"
            event.sent_at = datetime.utcnow()
            self.db.commit()
    
    def mark_as_error(self, event_id: int, error_message: str = None):
        event = self.db.query(OutboxEvent).filter(
            OutboxEvent.event_id == event_id
        ).first()
        
        if event:
            event.status = "error"
            if error_message:
                event.payload_json = f"ERROR: {error_message}"
            self.db.commit()
    
    def get_events_by_aggregate(self, aggregate_type: str, aggregate_id: int) -> List[OutboxEvent]:
        return self.db.query(OutboxEvent).filter(
            OutboxEvent.aggregate_type == aggregate_type,
            OutboxEvent.aggregate_id == aggregate_id
        ).all()
