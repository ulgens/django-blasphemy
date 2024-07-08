from django.db import models

from core.models import BaseModel

from .choices import LANGUAGE_CHOICES, STYLE_CHOICES


class Snippet(BaseModel):
    title = models.CharField(
        max_length=128,
        blank=True,
        default="",
    )
    code = models.TextField()
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        default="python",
        max_length=128,
    )
    style = models.CharField(
        choices=STYLE_CHOICES,
        default="friendly",
        max_length=128,
    )

    class Meta:
        ordering = ("-created_at",)
