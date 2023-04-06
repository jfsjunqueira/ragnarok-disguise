from django.db import models
from django.utils import timezone

# Create your models here.
class Monster(models.Model):
    name = models.CharField(max_length=255)
    sprite = models.ImageField(upload_to='sprites/')

    def __str__(self):
        return self.name

class LeaderboardEntry(models.Model):
    player_name = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-score', 'timestamp']