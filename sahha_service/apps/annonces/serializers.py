from rest_framework import serializers
from .models import Annonce, Categorie, Agence, TimeSlot


class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = [
            "id",
            "title",
            "description",
            "created",
            "updated",
            "user",
            "based_category",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["id", "name"]


class AgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agence
        fields = ["id", "city", "name", "address"]


class SlotSerializer((serializers.ModelSerializer)):
    class Meta:
        model = TimeSlot
        fields = [
            "id",
            "annonce_id",
            "description",
            "created",
            "start_time",
            "end_time",
            "is_periodic",
            "periodicity"
        ]
