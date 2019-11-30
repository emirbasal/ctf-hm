from django.db import models
from django.contrib.auth.models import AbstractUser
from challenges.models import Challenge
from django.contrib.auth.hashers import make_password


class Team(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    done_challenges = models.ManyToManyField(Challenge, blank=True)
    time_of_last_right_submission = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        hashed_password = make_password(self.password)
        self.password = hashed_password

        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class User(AbstractUser):
    points = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    # Könnte maybe entfernt werden. Reduntat TODO
    done_challenges = models.ManyToManyField(Challenge, blank=True)

    def __str__(self):
        return self.username
