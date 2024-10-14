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
from .models import Facultad
from .models import Matricula
from .models import HistorialAcademico
from .models import Conversacion
from .models import Mensaje
from rest_framework.authtoken.models import Token
from .serializers import EstudiantesSerializer, MensajeSerializer
from .serializers import ConversacionSerializer
from openai import OpenAI
from django.conf import settings
from datetime import date
from datetime import datetime
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
    serializer = EstudiantesSerializer(instance=estudiante)

    return Response({"estudiante": serializer.data}, status=status.HTTP_200_OK) 


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

    # OpenAI API Setup (assuming you have your API key stored securely)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Get Authenticated Student (assuming your authentication is working)
    auth_header = get_authorization_header(request).decode('utf-8')
    token_key = auth_header.split(' ')[1]
    try:
        token = EstudianteToken.objects.get(key=token_key)
        estudiante = token.estudiante
    except EstudianteToken.DoesNotExist:
        return Response({"error": "Token no válido"}, status=401)

    # 1. Context-Aware Information Retrieval:
    student_context = get_student_context(estudiante)

    # 2. Enhanced Prompt Engineering:
    full_prompt = f"{student_context}\nPregunta del estudiante: {prompt}"

    # 3. OpenAI API Call:
    try:
        response = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:tesis-rr:AI44COj5",  # Or the model you are using
            messages=[
                {"role": "system", "content": "Eres un asistente educativo que ayuda a los estudiantes con información de la universidad."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.5,
            max_tokens=1000,
        )
        final_response = response.choices[0].message.content.strip()

        return Response({"response": final_response}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)





def get_student_context(estudiante):
    """Builds a context string with relevant student information."""

    context = f"Estudiante: {estudiante.nombres} {estudiante.apellidos}\n"
    context += f"ID Estudiante: {estudiante.codigo_estudiante}\n"
    context += f"Carrera: {estudiante.id_carrera.nombre_carrera}\n"
    context += f"Facultad: {estudiante.id_carrera.id_facultad.nombre_facultad}\n"
    context += f"Estado Académico: {estudiante.estado_academico}\n"
    context += f"Ciclo Actual: {estudiante.ciclo_actual}\n"

    # Payment Information
    pagos = Pago.objects.filter(estudiante=estudiante)
    if pagos:
        context += "Pagos:\n"
        for pago in pagos:
            context += f"- {pago.tipo_pago}: {pago.estado} ({pago.monto} soles)\n"
    else:
        context += "No se encontraron pagos.\n"

    # Course Information (Example - you can customize this)
    matriculas = Matricula.objects.filter(id_estudiante=estudiante)
    if matriculas:
        context += "Cursos Matriculados:\n"
        for matricula in matriculas:
            curso = matricula.id_plan_estudio_curso.id_curso
            context += f"- {curso.nombre_curso} (Ciclo: {matricula.ciclo}, Semestre: {matricula.semestre})\n"

    # Academic History (Example)
    historial = HistorialAcademico.objects.filter(id_estudiante=estudiante)
    if historial:
        context += "Historial Académico:\n"
        for registro in historial:
            context += f"- {registro.id_curso.nombre_curso}: {registro.nota} (Semestre: {registro.semestre})\n"

    return context


##Guardar mensajes y crear conversacion
@api_view(["POST"])
@authentication_classes([EstudianteTokenAuthentication])
@permission_classes([IsAuthenticated])
def mensajeCreate(request):
    """Guarda mensajes a una conversación y devuelve mensajes ordenados."""

    conversacion_id = request.data.get('conversacion_id') 
    mensaje_texto = request.data.get('mensaje')  
    tipo_mensaje = request.data.get('tipo', 'user')  

    if not conversacion_id or not mensaje_texto:
        return Response({"error": "ID de Conversación y Mensaje son requeridos"}, status=400)

    try:
        conversacion = Conversacion.objects.get(id=conversacion_id)
    except Conversacion.DoesNotExist:
        conversacion = Conversacion.objects.create() 

    mensaje = Mensaje.objects.create(
        conversacion=conversacion,
        prompt=mensaje_texto,
        tipo=tipo_mensaje
    )

    # ordenar mensajes por fecha
    mensajes = conversacion.mensajes.all().order_by('fecha_hora')

    # dando formato a los mensajes con serialize
    serialized_mensajes = MensajeSerializer(mensajes, many=True).data 

    return Response({
        "message": "Mensaje guardado correctamente",
        "conversacion_id": conversacion.id,
        "mensaje_id": mensaje.id,
        "mensajes": serialized_mensajes  # respuesta con mensajes ordenados
    }, status=201)



@api_view(["POST"]) 
@authentication_classes([EstudianteTokenAuthentication]) 
@permission_classes([IsAuthenticated]) 
def conversacionCreate(request): 
    """Creates a new conversation for the authenticated student.""" 
    estudiante = request.user
    idConversacion = request.data.get('conversacion_id')

    # No need to fetch the student again, you already have it from request.user
    conversacion = Conversacion.objects.create(
        id=idConversacion,
        estudiante=estudiante,  # Directly assign the authenticated student
        fecha_inicio=datetime.now() 
    ) 

    # No need for the if conversacion check, create() will raise an exception if it fails
    return Response({ 
        "message": "Conversación creada correctamente", 
        "conversacion_id": conversacion.id 
    }, status=201) 


###OBTENER CONVERSACIONES:
@api_view(["POST"])
@authentication_classes([EstudianteTokenAuthentication])
@permission_classes([IsAuthenticated])
def getConversations(request):
    estudiante = request.user
    conversaciones = Conversacion.objects.filter(estudiante=estudiante)

    # Add last_message to each conversation
    for conversacion in conversaciones:
        last_message = conversacion.mensajes.order_by("-fecha_hora").first()
        conversacion.last_message = last_message

    # Serialize all conversations AFTER the loop
    serializer = ConversacionSerializer(conversaciones, many=True)  
    return Response(serializer.data, status=200)

##OBTENER MENSAJES DE CONVERSACIONES
@api_view(["POST"])
@authentication_classes([EstudianteTokenAuthentication])                                
@permission_classes([IsAuthenticated])
def getMessages(request):
    messages = Mensaje.objects.filter(conversacion=request.data.get('conversacion_id')).order_by(
        'fecha_hora')
    serializer = MensajeSerializer(messages, many=True)
    return Response(serializer.data, status=200)

#def chatbot(request):
 ##   prompt = request.data.get('prompt')
   # if not prompt:
#        return Response({"error": "Prompt is required"}, status=400)

    #openai.api_key = settings.OPENAI_API_KEY
    #client = openai
    # Get the authenticated student
  #  auth_header = get_authorization_header(request).decode('utf-8')
 #   token_key = auth_header.split(' ')[1]
   # try:
    #    token = EstudianteToken.objects.get(key=token_key)
     #   estudiante = token.estudiante
    #except EstudianteToken.DoesNotExist:
     #   raise AuthenticationFailed('Token no válido')

    # Initialize the response
    #db_response = "Lo siento, no entiendo la pregunta."

    # Extract relevant information
    #if "curso" in prompt.lower():
        #curso_nombre = prompt.split("curso")[-1].strip()
        #try:
     #       curso = Curso.objects.get(nombre_curso__icontains=curso_nombre)
      #      db_response = f"Curso: {curso.nombre_curso}, Descripción: {curso.descripcion}, Créditos: {curso.creditos}, Modalidad: {curso.modalidad}"
       # except Curso.DoesNotExist:
        #    db_response = "No se encontró un curso con ese nombre."

    #elif "estado académico" in prompt.lower():
     #   db_response = f"Estudiante: {estudiante.nombres} {estudiante.apellidos}, Estado: {estudiante.estado_academico}, Ciclo actual: {estudiante.ciclo_actual}"

    #elif "pago" in prompt.lower():
     #   pagos = Pago.objects.filter(estudiante=estudiante)
      #  if pagos.exists():
       #     db_response = f"Pagos para {estudiante.nombres}: " + ", ".join([f"{p.tipo_pago}: {p.estado} ({p.monto} soles)" for p in pagos])
        #else:
         #   db_response = "No se encontraron pagos."

    # Refine response using OpenAI API
    #try:
     #   client= OpenAI(api_key=settings.OPENAI_API_KEY)
      #  gtp_model="gpt-3.5-turbo",
       # messages=[
        #        {"role": "system", "content": "You are a helpful educational assistant."},
         #       {"role": "user", "content": f"{prompt}"},
          #      {"role": "assistant", "content": db_response}
           # ]
        
       # response = client.chat.completions.create(
        #   model=gtp_model,
         #  messages=messages,
          # temperature=0.5,
           #max_tokens=1000,
        #)
        #final_response = response.choices[0].message.content.strip()
        #return Response({"response": final_response}, status=200)

   # except Exception as e:
    #    return Response({"error": str(e)}, status=500)
    