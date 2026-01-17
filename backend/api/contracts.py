from typing import List, Optional, Any, Dict
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from django.db import transaction
from django.contrib.auth.models import User
from core.models import Contract, ContractFieldValue, Blueprint, ContractStatusHistory

router = APIRouter()

# Pydantic Models for Contract
class ContractCreate(BaseModel):
    blueprint_id: int
    # In a real app, user might be inferred from auth token
    user_id: int 

class ContractTransition(BaseModel):
    new_status: str
    # user_id performing action
    user_id: int

class FieldValueUpdate(BaseModel):
    field_label: str
    value: str

class ContractUpdateFields(BaseModel):
    values: List[FieldValueUpdate]

# Helpers
def format_contract(c):
    return {
        "id": c.id,
        "blueprint_title": c.blueprint.title,
        "body_text": c.blueprint.body_text,
        "status": c.status,
        "created_by": c.created_by.username,
        "created_at": str(c.created_at),
        "fields": [
            {
                "label": fv.field.label,
                "field_type": fv.field.field_type,
                "pos_x": fv.field.pos_x,
                "pos_y": fv.field.pos_y,
                "position_label": fv.field.position_label,
                "value": fv.value
            }
            for fv in c.field_values.all()
        ]
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_contract(data: ContractCreate):
    try:
        blueprint = Blueprint.objects.get(pk=data.blueprint_id)
        user = User.objects.get(pk=data.user_id) # Simplify: assumes user exists
    except (Blueprint.DoesNotExist, User.DoesNotExist):
        raise HTTPException(status_code=404, detail="Blueprint or User not found")

    with transaction.atomic():
        contract = Contract.objects.create(
            blueprint=blueprint,
            created_by=user,
            status='CREATED'
        )
        # Initialize fields
        for field in blueprint.fields.all():
            ContractFieldValue.objects.create(
                contract=contract,
                field=field,
                value=""
            )
        
        # Log history
        ContractStatusHistory.objects.create(
            contract=contract,
            new_status='CREATED',
            changed_by=user
        )
        
    return format_contract(contract)

@router.get("/")
def list_contracts(status: Optional[str] = None):
    qs = Contract.objects.all().select_related('blueprint', 'created_by').prefetch_related('field_values__field')
    if status:
        qs = qs.filter(status=status.upper())
    return [format_contract(c) for c in qs]

@router.get("/{contract_id}")
def get_contract(contract_id: int):
    try:
        c = Contract.objects.select_related('blueprint', 'created_by').prefetch_related('field_values__field').get(pk=contract_id)
        return format_contract(c)
    except Contract.DoesNotExist:
        raise HTTPException(status_code=404, detail="Contract not found")

@router.post("/{contract_id}/transition")
def transition_contract(contract_id: int, data: ContractTransition):
    try:
        c = Contract.objects.get(pk=contract_id)
        user = User.objects.get(pk=data.user_id)
    except (Contract.DoesNotExist, User.DoesNotExist):
        raise HTTPException(status_code=404, detail="Contract or User not found")

    current = c.status
    nxt = data.new_status.upper()
    
    # Strict Lifecycle: Created -> Approved -> Sent -> Signed -> Locked
    # Revoked allowed from Created or Sent
    valid_transitions = {
        'CREATED': ['APPROVED', 'REVOKED'],
        'APPROVED': ['SENT'],
        'SENT': ['SIGNED', 'REVOKED'],
        'SIGNED': ['LOCKED'],
        'LOCKED': [],
        'REVOKED': []
    }
    
    if nxt not in valid_transitions.get(current, []):
        raise HTTPException(status_code=400, detail=f"Invalid transition from {current} to {nxt}")

    with transaction.atomic():
        c.status = nxt
        c.save()
        ContractStatusHistory.objects.create(
            contract=c,
            previous_status=current,
            new_status=nxt,
            changed_by=user
        )
    
    return {"status": "success", "new_status": c.status}

@router.patch("/{contract_id}/fields")
def update_contract_fields(contract_id: int, data: ContractUpdateFields):
    try:
        c = Contract.objects.get(pk=contract_id)
    except Contract.DoesNotExist:
        raise HTTPException(status_code=404, detail="Contract not found")

    if c.status in ['LOCKED', 'REVOKED']:
        raise HTTPException(status_code=400, detail="Cannot edit locked or revoked contracts")

    with transaction.atomic():
        for item in data.values:
            # We search by label for simplicity in MVP, ideally use field ID
            fv = c.field_values.filter(field__label=item.field_label).first()
            if fv:
                fv.value = item.value
                fv.save()
    
    return {"status": "updated"}
