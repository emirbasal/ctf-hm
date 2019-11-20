from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('challenges/', include('challenges.url')),
    path('api-auth', include('rest_framework.urls'))
]
