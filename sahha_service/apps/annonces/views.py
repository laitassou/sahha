from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Annonce, TimeSlot, Categorie, Agence
from .serializers import (
    AnnonceSerializer,
    CategorySerializer,
    AgenceSerializer,
    SlotSerializer,
)
from rest_framework import permissions
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication


class AnnoncesListView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    # 1. List all
    def get(self, request, *args, **kwargs):
        """
        List all items for given requested user
        """
        annonces = Annonce.objects.filter(user=request.user.id)
        serializer = AnnonceSerializer(annonces, many=True)
        ##print("serializer.data:", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        """
        Create the annonce with given data
        """
        data = {
            "title": request.data.get("title"),
            "description": request.data.get("description"),
            "user": request.user.id,
        }
        serializer = AnnonceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnonceDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_object(self, ads_id, user_id):
        """
        Helper method to get the object with given ads_id, and user_id
        """
        try:
            data = Annonce.objects.filter(id=ads_id, user=user_id)
            print("data", data)
            return data
        except Annonce.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, ads_id, *args, **kwargs):
        """
        Retrieves the annonce with given id
        """
        ads_instance = self.get_object(ads_id, request.user.id)
        if not ads_instance:
            return Response(
                {"res": "Object with ads_id id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AnnonceSerializer(ads_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, ads_id, *args, **kwargs):
        """
        Updates the todo item with given todo_id if exists
        """
        ads_instance = self.get_object(ads_id, request.user.id)
        if not ads_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "title": request.data.get("title"),
            "updated": request.data.get("updated"),
            "user": request.user.id,
        }
        serializer = AnnonceSerializer(instance=ads_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, ads_id, *args, **kwargs):
        """
        Deletes the todo item with given todo_id if exists
        """
        ads_instance = self.get_object(ads_id, request.user.id)
        if not ads_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ads_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)


class SlotListView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    # 1. List all
    def get(self, request, ads_id, *args, **kwargs):
        """
        List all items for given requested user
        """
        print("laa request:", request)
        slots = TimeSlot.objects.all().select_related("annonce_id")
        serializer = SlotSerializer(slots, many=True)
        print("serializer.data:", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        """
        Create slot with given data
        """
        print("la post request:", request)
        data = {
            "annonce_id": request.annonce.id,
            "description": request.data.get("description"),
            "user": request.user.id,
        }
        serializer = SlotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    authentication_classes = ()

    # 1. List all
    def get(self, request, *args, **kwargs):
        """
        List all categories
        """
        category = Categorie.objects
        serializer = CategorySerializer(category, many=True)
        ##print("serializer.data:", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AgencesListView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    authentication_classes = ()

    # 1. List all
    def get(self, request, *args, **kwargs):
        """
        List all categories
        """
        agences = Agence.objects
        serializer = AgenceSerializer(agences, many=True)
        ##print("serializer.data:", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
