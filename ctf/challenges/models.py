from django.db import models


class ChallengeType(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Challenge(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=100, blank=False)
    points = models.PositiveSmallIntegerField(blank=False)
    flag = models.CharField(max_length=200, null=True)
    challenge_type = models.ForeignKey(ChallengeType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
