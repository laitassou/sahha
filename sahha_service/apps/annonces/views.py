from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Annonce, TimeSlot, Categorie, Agence, Intervention

from ...models import SahhaUser
from ..users.serializers import SahhaUserSerializer


from .serializers import (
    AnnonceSerializer,
    CategorySerializer,
    AgenceSerializer,
    SlotSerializer,
    InterventionSerializer,
    SlotAdsSerializer,
)

from rest_framework import permissions
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication


class AnnoncesListView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    # 1. List all
    def get(self, request, user_id=None, *args, **kwargs):
        """
        List all items for given requested user
        """

        if user_id is not None:
            manager = SahhaUser.objects.get(django_user=request.user)

            manager_serializer = SahhaUserSerializer(manager)
            role = manager_serializer.data.get('role', None)
            agence = manager_serializer.data.get('agence_id', None)

            if role != 'Manager':
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            annonces = Annonce.objects.filter(user=user_id)
            serializer = AnnonceSerializer(annonces, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)            

        else:            
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
            "addresse": request.data.get("address"),
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
        Updates the annonce item with given a if exists
        """
        ads_instance = self.get_object(ads_id, request.user.id)
        if not ads_instance:
            return Response(
                {"res": "Object with ads_id does not exists"},
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
        Deletes the annonce item with given ads_id if exists
        """
        ads_instance = self.get_object(ads_id, request.user.id)
        if not ads_instance:
            return Response(
                {"res": "Object with ads_id does not exists"},
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
        annonce = Annonce.objects.filter(id=ads_id,)
        ads_serializer = AnnonceSerializer(annonce, many=True)
        ads = ads_serializer.data
        slots = TimeSlot.objects.filter(annonce_id=ads_id,).select_related('time_slot_intervenant')
        serializer = SlotSerializer(slots, many=True)
        #add ads in first position
        data = serializer.data
        data.append(ads)
        return Response(data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, ads_id,  *args, **kwargs):
        """
        Create slot with given data
        """
        data = {
            "annonce_id": ads_id,
            "description": request.data.get("description"),
            "start_time": request.data.get("start_time"),
            "end_time": request.data.get("end_time"),
            "user": request.user.id,
        }
        serializer = SlotSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # 3. Update
    def put(self, request, ads_id, *args, **kwargs):
        """
        Updates the slot item with given ads_id if exists
        """
        ads_instance = self.get_object(ads_id, request.user.id)
        if not ads_instance:
            return Response(
                {"res": "Object with ads_id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "intervenant_id": request.data.get("intervenant_id"),
            "updated": request.data.get("updated"),

        }
        serializer = SlotSerializer(instance=ads_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlotView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_object(self, slot_id):
        """
        Helper method to get the object with given ads_id
        """
        try:
            data = TimeSlot.objects.filter(id=slot_id,)
            return data
        except TimeSlot.DoesNotExist:
            return None
        
    # 1. get
    def get(self, request, slot_id, *args, **kwargs):
        """
        Get given slot for given requested user
        """
        slot = TimeSlot.objects.filter(id=slot_id,)
        serializer = SlotSerializer(slot, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)



    # 2. Update
    def put(self, request, slot_id, ads_id, worker_id, *args, **kwargs):
        """
        Updates the slot item with given slot_id if exists
        """

    
        user = SahhaUser.objects.get(django_user=request.user)

        serializer = SahhaUserSerializer(user)
        role = serializer.data.get('role', None)

        if role is None or  role != SahhaUser.MANAGER:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        slot_instance = TimeSlot.objects.get(id=slot_id,annonce_id=ads_id)
        
        if not slot_instance:
            return Response(
                {"res": "Object with  slot_id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "time_slot_intervenant": worker_id,
        }
        serializer = SlotSerializer(instance=slot_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlotListPerWorkerView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    # 1. List all
    def get(self, request, worker_id, *args, **kwargs):
        """
        List all items for given worker
        """
        slots = TimeSlot.objects.filter(time_slot_intervenant=worker_id)
        serializer = SlotAdsSerializer(slots, many=True)
        #add ads in first position
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    


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
    


class InterventionView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_object(self, slot_id):
        """
        Helper method to get the object with given ads_id
        """
        try:
            data = Intervention.objects.filter(id=slot_id,)
            return data
        except TimeSlot.DoesNotExist:
            return None
        
    # 1. get
    def get(self, request, slot_id, worker_id, *args, **kwargs):
        """
        Get given slot for given requested user
        """
        slot = Intervention.objects.filter(id=worker_id,)
        serializer = SlotSerializer(slot, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)




    # 3. create
    def post(self, request, slot_id, worker_id, *args, **kwargs):
        """
        Updates the slot item with given slot_id if exists
        """

        user = SahhaUser.objects.get(django_user=request.user)

        serializer = SahhaUserSerializer(user)
        role = serializer.data.get('role', None)
        if role is None or  role != SahhaUser.Client:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        slot_instance = TimeSlot.objects.get(id=slot_id)
        if not slot_instance:
            return Response(
                {"res": "Object with  slot_id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        slot_serializer = SlotSerializer(slot_instance)
        data = slot_serializer.data
        id = data.get('intervenant', {}).get('id')
        django_id = data.get('intervenant', {}).get('django_id')

        print("laa data", data)
       
        if id != worker_id:
            return Response(
                {"res": "Bad worker id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
                    
        
        data = {
            "slot_id": slot_id,
            "intervenant": django_id,
            "reporting": request.data.get("feedback"),
            "score": request.data.get("score"),
            "done": True,

        }
        serializer = InterventionSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

