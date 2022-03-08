from django.db import models

class PublishedStateOptions(models.TextChoices):
    PUBLISH = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'
