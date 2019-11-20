from django.db import models
from django.contrib.auth.models import AbstractUser
from challenges.models import Challenge

class Team(models.Model):
    name = models.CharField(max_length=20)
    points = models.IntegerField(default=0)
    done_challenges = models.ManyToManyField(Challenge, null=True, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    points = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    # Könnte maybe entfernt werden. Reduntat TODO
    done_challenges = models.ManyToManyField(Challenge, null=True, blank=True)

    def __str__(self):
        return self.username
