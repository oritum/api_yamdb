from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin

from api.serializers import SignupSerializer
from reviews.models import User

