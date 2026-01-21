from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from django.db import transaction
from core.models import Blueprint, BlueprintField

router = APIRouter()

# Pydantic Models
class FieldSchema(BaseModel):
    label: str
    field_type: str
    pos_x: int
    pos_y: int
    pos: Optional[str] = None # 'top-left', 'top-right', etc.

class BlueprintCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    body_text: Optional[str] = "" # For contract body
    fields: List[FieldSchema]

class BlueprintResponse(BaseModel):
    id: int
    title: str
    description: str
    body_text: str
    created_at: str
    fields: List[FieldSchema]

    class Config:
        from_attributes = True

# Helper to convert Django types
def format_blueprint(bp):
    return {
        "id": bp.id,
        "title": bp.title,
        "description": bp.description,
        "body_text": bp.body_text,
        "created_at": str(bp.created_at),
        "fields": list(bp.fields.values('label', 'field_type', 'pos_x', 'pos_y', 'position_label'))
    }

@router.get("/", response_model=List[BlueprintResponse])
def list_blueprints():
    # We can't use response_model directly with Django querysets easily without conversion
    # unless using a library like pydantic-django or similar.
    # Manual conversion for MVP safety.
    blueprints = Blueprint.objects.all().prefetch_related('fields')
    return [format_blueprint(bp) for bp in blueprints]

@router.post("/", response_model=BlueprintResponse, status_code=status.HTTP_201_CREATED)
def create_blueprint(data: BlueprintCreate):
    with transaction.atomic():
        bp = Blueprint.objects.create(
            title=data.title,
            description=data.description,
            body_text=data.body_text
        )
        for field in data.fields:
            BlueprintField.objects.create(
                blueprint=bp,
                label=field.label,
                field_type=field.field_type,
                pos_x=field.pos_x,
                pos_y=field.pos_y,
                position_label=field.pos
            )
    return format_blueprint(bp)

@router.get("/{blueprint_id}", response_model=BlueprintResponse)
def get_blueprint(blueprint_id: int):
    try:
        bp = Blueprint.objects.prefetch_related('fields').get(pk=blueprint_id)
        return format_blueprint(bp)
    except Blueprint.DoesNotExist:
        raise HTTPException(status_code=404, detail="Blueprint not found")
