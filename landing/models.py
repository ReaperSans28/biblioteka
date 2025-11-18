from django.db import models
from django.db.models import CharField, TextField, DateTimeField


class Item(models.Model):
    name = CharField(max_length=255)
    description = TextField(blank=True)
    created_at = DateTimeField(auto_now=True)
