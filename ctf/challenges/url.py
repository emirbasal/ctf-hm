from django.urls import path
from . import views
from rest_framework import routers
from .api import (
    ChallengeListViewSet,
    ChallengeTypeListViewSet,
    ChallengeCreateViewSet,
    ChallengeTypeCreateViewSet,
    # ChallengeDetailViewSet
)

# router = routers.DefaultRouter()
# # Neue Routen müssen hier registriert werden
# router.register('api/challenges', ChallengeListViewSet, base_name='challenge_list')
# router.register('api/challenges/create', ChallengeCreateViewSet, base_name='challenge_create')
# router.register('api/challengetypes', ChallengeTypeListViewSet, base_name='challengeType_list')
# router.register('api/challengetypes/create', ChallengeTypeCreateViewSet, base_name='challengeType_create')
#
# urlpatterns = router.urls

urlpatterns = [
    # path('', views.home, name='home'),
    path('challenges', views.ChallengeListView.as_view(), name='challenges'),
    path('challenges/<int:pk>', views.ChallengeDetail.as_view(), name='challenge_detail'),
    path('challenges/<int:pk>/file', views.download, name='challenge_file_download')
]

