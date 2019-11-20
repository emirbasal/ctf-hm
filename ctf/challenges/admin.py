from django.contrib import admin
from .models import Challenge, ChallengeType


models = [Challenge, ChallengeType]

for model in models:
    admin.site.register(model)
