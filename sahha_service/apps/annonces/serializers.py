from rest_framework import serializers
from .models import Annonces

class AnnoncesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonces
        fields = ["title", "description", "created", "updated", "user"]