import json

from django.core import serializers
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.mixins import UpdateModelMixin
from omnipresence.models import OmnipresenceModel
from omnipresence.serializer import OmnipresenceSerializer


class OmnipresenceView(GenericAPIView):
    """
    Omnipresence Management View

    Provides endpoints for retrieving and creating OmnipresenceModel instances.

    Features:
        - Retrieve character information by 'charname'
        - Create new OmnipresenceModel instances

    Endpoints:
        - GET: Retrieve character details
        - POST: Create a new character

    Parameters:
        - Request Body (POST):
            * username (str): Username of the character
            * charname (str): Character name
            * working_dir (str): Working directory of the character

    Responses:
        - HTTP 200: Successful retrieval
        - HTTP 201: Successful creation
        - HTTP 400: Validation errors
    """
    queryset = OmnipresenceModel.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Retrieve character information based on 'charname' query parameter.

        Parameters:
            - charname (str): Query parameter to filter characters

        Returns:
            - HttpResponse: JSON response with character details or empty dictionary
        """
        character = OmnipresenceModel.objects.filter(
            charname = request.GET.get('charname')
        ).values('pk', 'username', 'charname', 'working_dir', 'is_active')
        if character:
            return HttpResponse(
                json.dumps(list(character)),
                status = 200,
                content_type = 'application/json'
        )
        return HttpResponse(json.dumps(dict()), status = 200, content_type = 'application/json')

    def post(self, request, *args, **kwargs):
        """
        Create a new OmnipresenceModel instance with the provided data.

        Parameters:
            - Request Body:
                * username (str): Username of the character
                * charname (str): Character name
                * working_dir (str): Working directory of the character

        Returns:
            - Response: HTTP 201 on success, HTTP 400 on validation errors
        """
        data = {
            'username': request.data.get('username'),
            'charname': request.data.get('charname'),
            'working_dir': request.data.get('working_dir')
        }
        serializer = OmnipresenceSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = 201)
        return Response(serializer.errors, status = 400)


class OmnipresenceActiveView(GenericAPIView):
    """
    Active Omnipresence Management View

    Provides endpoints for retrieving active OmnipresenceModel instances.

    Features:
        - Retrieve all active characters
        - Retrieve active characters by working directory

    Endpoints:
        - GET: Retrieve all active characters
        - POST: Retrieve active characters by working directory

    Parameters:
        - Request Body (POST):
            * cwd (str): Current working directory to filter active characters

    Responses:
        - HTTP 200: Successful retrieval
    """

    queryset = OmnipresenceModel.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Retrieve all active characters.

        Returns:
            - HttpResponse: JSON response with active character details
        """
        actives = OmnipresenceModel.objects.filter(
            is_active = True
        ).values('username','charname')
        return HttpResponse(
            json.dumps(list(actives)),
            status = 200,
            content_type = 'application/json'
        )

    def post(self, request, *args, **kwargs):
        """
        Retrieve active characters based on the current working directory.

        Parameters:
            - Request Body:
                * cwd (str): Current working directory to filter active characters

        Returns:
            - HttpResponse: JSON response with active character details
        """
        local_actives = OmnipresenceModel.objects.filter(
            working_dir = request.data.get('cwd')
        ).values('charname')
        return HttpResponse(
            json.dumps(list(local_actives)),
            status = 200,
            content_type = 'application/json'
        )


class OmnipresenceUpdateView(GenericAPIView, UpdateModelMixin):
    """
    Omnipresence Update View

    Provides an endpoint for updating OmnipresenceModel instances.

    Features:
        - Partial updates for OmnipresenceModel instances

    Endpoint:
        - PATCH: Partially update an OmnipresenceModel instance

    Parameters:
        - Request Body (PATCH): Fields to update

    Responses:
        - HTTP 200: Successful update
        - HTTP 400: Validation errors
    """
    queryset = OmnipresenceModel.objects.all()
    serializer_class = OmnipresenceSerializer

    def patch(self, request, *args, **kwargs):
        """
        Partially update an Omnipresencemodel instance.

        Parameters:
            - Request Body: Fields to update

        Returns:
            - Response: HTTP 200 on success, HTTP 400 on validation errors
        """
        return self.partial_update(request, *args, **kwargs)
