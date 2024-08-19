from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    anime_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('anime_id', 'user')

    def __str__(self):
        return f'Review by {self.user.username} for anime {self.anime_id}'
