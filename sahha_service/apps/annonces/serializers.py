from rest_framework import serializers
from .models import Annonce, Categorie, Agence, TimeSlot

from ..users.serializers import SahhaUserSerializer
from ...models import SahhaUser


class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = [
            "id",
            "title",
            "description",
            "created",
            "updated",
            "addresse",
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
        fields = "__all__"
        """[
            "id",
            "annonce_id",
            "description",
            #"time_slot_intervenant",
            "created",
            "start_time",
            "end_time",
            "is_periodic",
            "periodicity",
            "intervenant",
            ]
        """
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.time_slot_intervenant is not None:
            user = SahhaUser.objects.get(django_user=instance.time_slot_intervenant)
            rep["intervenant"] = SahhaUserSerializer(user).data
        return rep
