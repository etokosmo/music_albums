from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(['POST'])
def create_album(request):
    pass