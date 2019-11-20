from rest_framework import serializers
from .models import Challenge, ChallengeType


class ChallengeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'points', 'challenge_type']


class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'points', 'challenge_type']


class ChallengeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'


class ChallengeTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeType
        fields = ['title', 'description']


class ChallengeTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeType
        fields = '__all__'
