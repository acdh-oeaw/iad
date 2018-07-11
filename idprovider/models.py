from django.db import models


class IdProvider(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.CharField(
        max_length=20, blank=True, verbose_name='Username of the creator',
        help_text="Username of the object's creator."
    )
