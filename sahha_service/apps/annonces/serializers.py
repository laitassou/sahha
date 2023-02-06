from rest_framework import serializers
from .models import Annonce

class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = ["id", "title", "description", "created", "updated", "user", "based_category"]