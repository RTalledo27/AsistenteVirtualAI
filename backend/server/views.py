from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Estudiante
from .models import EstudianteToken
from .models import EstudianteTokenAuthentication
from .models import Curso
from .models import Pago


from rest_framework.authtoken.models import Token
from .serializers import EstudiantesSerializer
import openai
from django.conf import settings


from rest_framework.decorators import authentication_classes, permission_classes

from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication

from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

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


##CHATBOT REST API ROUTES
@api_view(["POST"])
@authentication_classes([EstudianteTokenAuthentication])
@permission_classes([IsAuthenticated])
def chatbot(request):
    prompt = request.data.get('prompt')
    if not prompt:
        return Response({"error": "Prompt is required"}, status=400)

    openai.api_key = settings.OPENAI_API_KEY
    client = openai
    # Get the authenticated student
    auth_header = get_authorization_header(request).decode('utf-8')
    token_key = auth_header.split(' ')[1]
    try:
        token = EstudianteToken.objects.get(key=token_key)
        estudiante = token.estudiante
    except EstudianteToken.DoesNotExist:
        raise AuthenticationFailed('Token no válido')

    # Initialize the response
    db_response = "Lo siento, no entiendo la pregunta."

    # Extract relevant information
    if "curso" in prompt.lower():
        curso_nombre = prompt.split("curso")[-1].strip()
        try:
            curso = Curso.objects.get(nombre_curso__icontains=curso_nombre)
            db_response = f"Curso: {curso.nombre_curso}, Descripción: {curso.descripcion}, Créditos: {curso.creditos}, Modalidad: {curso.modalidad}"
        except Curso.DoesNotExist:
            db_response = "No se encontró un curso con ese nombre."

    elif "estado académico" in prompt.lower():
        db_response = f"Estudiante: {estudiante.nombres} {estudiante.apellidos}, Estado: {estudiante.estado_academico}, Ciclo actual: {estudiante.ciclo_actual}"

    elif "pago" in prompt.lower():
        pagos = Pago.objects.filter(estudiante=estudiante)
        if pagos.exists():
            db_response = f"Pagos para {estudiante.nombres}: " + ", ".join([f"{p.tipo_pago}: {p.estado} ({p.monto} soles)" for p in pagos])
        else:
            db_response = "No se encontraron pagos."

    # Refine response using OpenAI API
    try:
        response =  client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant."},
                {"role": "user", "content": f"{prompt}"},
                {"role": "assistant", "content": db_response}
            ]
        )
        final_response = response['choices'][0]['message']['content'].strip()
        return Response({"response": final_response}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    