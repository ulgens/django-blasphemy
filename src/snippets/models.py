from django.db import models

from core.db.models import BaseModel

from .choices import LANGUAGE_CHOICES, STYLE_CHOICES


class Snippet(BaseModel):
    title = models.CharField(max_length=128)
    code = models.TextField()
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        default="python",
        max_length=128,
        db_index=True,
    )
    style = models.CharField(
        choices=STYLE_CHOICES,
        default="friendly",
        max_length=128,
        db_index=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_at",)
