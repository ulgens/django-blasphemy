from core.models import BaseModel
from django.db import models

from .choices import LANGUAGE_CHOICES, STYLE_CHOICES


class Snippet(BaseModel):
    title = models.CharField(
        max_length=128,
        blank=True,
        default="",
    )
    code = models.TextField()
    show_line_numbers = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        default="python",
        max_length=100,
    )
    style = models.CharField(
        choices=STYLE_CHOICES,
        default="friendly",
        max_length=100,
    )

    class Meta:
        ordering = ("-created_at",)
