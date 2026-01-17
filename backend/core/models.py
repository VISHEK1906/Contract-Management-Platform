from django.db import models
from django.contrib.auth.models import User

class Blueprint(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True) # Used for short description or internal notes
    body_text = models.TextField(blank=True, default='') # The full contract text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BlueprintField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('date', 'Date'),
        ('signature', 'Signature'),
        ('checkbox', 'Checkbox'),
    ]

    blueprint = models.ForeignKey(Blueprint, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)
    position_label = models.CharField(max_length=50, blank=True, null=True) # e.g. "top-left"

    def __str__(self):
        return f"{self.label} ({self.field_type})"

class Contract(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('APPROVED', 'Approved'),
        ('SENT', 'Sent'),
        ('SIGNED', 'Signed'),
        ('LOCKED', 'Locked'),
        ('REVOKED', 'Revoked'),
    ]

    blueprint = models.ForeignKey(Blueprint, related_name='contracts', on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, related_name='contracts', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contract {self.id} - {self.blueprint.title}"

class ContractFieldValue(models.Model):
    contract = models.ForeignKey(Contract, related_name='field_values', on_delete=models.CASCADE)
    field = models.ForeignKey(BlueprintField, related_name='contract_values', on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.contract} - {self.field.label}: {self.value}"

class ContractStatusHistory(models.Model):
    contract = models.ForeignKey(Contract, related_name='history', on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, related_name='status_changes', on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
