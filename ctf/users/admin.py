from django.contrib import admin
from .models import User, Team


models = [User, Team]
for model in models:
    admin.site.register(model)
