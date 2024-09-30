from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Estudiante
from .models import EstudianteToken
from .models import EstudianteTokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import EstudiantesSerializer

from rest_framework.decorators import authentication_classes, permission_classes

from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication

@api_view(["POST"])
def login(request):
    
    estudiante = get_object_or_404(Estudiante, user=request.data['username'])

    # Autenticar usuario de estudiante usando el correo institucional
    if not estudiante.check_password(request.data['password']):
        return Response({"error":"Credenciales invalidas"}, status=status.HTTP_401_UNAUTHORIZED)
    

    #CREAR TOKEN PARA EL ESTUDIANTE ASOCIADO
    

    token, created = EstudianteToken.objects.get_or_create(estudiante = estudiante)
    

    serializer = EstudiantesSerializer(instance=estudiante)

    return Response({"token":token.key,'estudiante':serializer.data},status=status.HTTP_200_OK)
    

@api_view(["POST"])
@authentication_classes([EstudianteTokenAuthentication])
@permission_classes([IsAuthenticated])
def getData(request):
    estudiante = request.user  # Esto ahora es el estudiante autenticado
    return Response(f"Sesión iniciada con: {estudiante.user}", status=status.HTTP_200_OK)




@api_view(["POST"])
def register(request):
    return


@api_view(["POST"])
def profile(request):
    return Response({})