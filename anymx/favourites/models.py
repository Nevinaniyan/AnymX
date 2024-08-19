from django.conf import settings
from django.db import models


class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    anime_id = models.IntegerField(null=True, blank=True)
    character_id = models.IntegerField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime_id', 'character_id')

    def __str__(self):
        return f"{self.user.username} - {self.anime_id if self.anime_id else self.character_id}"
