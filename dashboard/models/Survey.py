from django.utils import timezone
from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def is_expired(self) -> bool:
        if self.expires_at:
            return self.expires_at < timezone.now()
        return False