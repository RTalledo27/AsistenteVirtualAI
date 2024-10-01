from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
import secrets
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.db import models
#### Modelos para la Universidad ####

# Facultad model
class Facultad(models.Model):
    nombre_facultad = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_facultad

# Carrera model
class Carrera(models.Model):
    id_facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    nombre_carrera = models.CharField(max_length=255)
    descripcion = models.TextField()
    duracion = models.IntegerField()

    def __str__(self):
        return self.nombre_carrera

# PlanEstudio model
class PlanEstudio(models.Model):
    id_carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    nombre_plan = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return f"Plan de Estudio: {self.nombre_plan} - {self.id_carrera.nombre_carrera}"

# Curso model
class Curso(models.Model):
    nombre_curso = models.CharField(max_length=255)
    descripcion = models.TextField()
    creditos = models.DecimalField(max_digits=10, decimal_places=2)
    TIPO_CURSO_CHOICES = [
        ('obligatorio', 'Obligatorio'),
        ('optativo', 'Optativo'),
    ]
    tipo_curso = models.CharField(max_length=12, choices=TIPO_CURSO_CHOICES)

    MODALIDAD_CHOICES = [
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
        ('híbrido', 'Híbrido'),
    ]
    modalidad = models.CharField(max_length=255, choices=MODALIDAD_CHOICES)

    def __str__(self):
        return self.nombre_curso

# PlanEstudioCurso model
class PlanEstudioCurso(models.Model):
    id_plan_estudio = models.ForeignKey(PlanEstudio, on_delete=models.CASCADE)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ciclo = models.IntegerField()  # Indica en qué ciclo se debe tomar el curso
    semestre = models.IntegerField()  # Indica en qué semestre se debe tomar el curso

    def __str__(self):
        return f"{self.id_plan_estudio.nombre_plan} - {self.id_curso.nombre_curso} (Ciclo {self.ciclo}, Semestre {self.semestre})"

#### Modelos para el Estudiante ####

# Estudiante model
class Estudiante(models.Model):
    id_carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    user = models.CharField(max_length=15)
    codigo_estudiante = models.IntegerField()
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    correo_electronico = models.EmailField(max_length=255)
    correo_institucional = models.EmailField(max_length=255)
    contrasena = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255)
    telefono = models.IntegerField()
    fecha_ingreso = models.DateField(null=True, blank=True)
    ESTADO_ACADEMICO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('graduado', 'Graduado'),
        ('expulsado', 'Expulsado'),
    ]
    estado_academico = models.CharField(max_length=255, choices=ESTADO_ACADEMICO_CHOICES)
    ciclo_actual = models.IntegerField()

    def save(self, *args, **kwargs):
        # Hashear la contraseña antes de guardar si es nueva o fue modificada
        if not self.pk or self.has_changed('contrasena'):
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.contrasena)
    
    def has_changed(self, field):
        if not self.pk:
            return True
        old_value = type(self).objects.get(pk=self.pk).__dict__[field]
        return getattr(self, field) != old_value
    
    # Método para simular la autenticación
    @property
    def is_authenticated(self):
        return True
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class EstudianteToken(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(20)  # Genera un token aleatorio
        super().save(*args, **kwargs)
    
class EstudianteTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Obtener el token del encabezado 'Authorization'
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Verificar que el encabezado tenga el formato adecuado 'Token <clave>'
        try:
            token_key = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed('Encabezado de token inválido')

        # Buscar el token en la base de datos
        try:
            token = EstudianteToken.objects.get(key=token_key)
        except EstudianteToken.DoesNotExist:
            raise AuthenticationFailed('Token no válido')

        # Retornar el estudiante asociado al token
        return (token.estudiante, None)

# Matricula model
class Matricula(models.Model):
    id_estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    id_plan_estudio_curso = models.ForeignKey(PlanEstudioCurso, on_delete=models.CASCADE)  # Relaciona con la tabla intermedia
    ciclo = models.IntegerField()
    semestre = models.IntegerField()
    estado = models.CharField(max_length=255)

    def __str__(self):
        return f"Matricula de {self.id_estudiante.nombres} en {self.id_plan_estudio_curso.id_curso.nombre_curso} (Ciclo {self.ciclo}, Semestre {self.semestre})"

# Historial Academico model
class HistorialAcademico(models.Model):
    id_estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(null=True, blank=True)
    semestre = models.IntegerField()

    def __str__(self):
        return f"Historial de {self.id_estudiante.nombres} para {self.id_curso.nombre_curso}"

# Requisitos Previos model
class RequisitosPrevios(models.Model):
    id_curso = models.ForeignKey(Curso, related_name='curso', on_delete=models.CASCADE)
    id_curso_requisito = models.ForeignKey(Curso, related_name='curso_requisito', on_delete=models.CASCADE)

    def __str__(self):
        return f"Requisito {self.id_curso_requisito.nombre_curso} para {self.id_curso.nombre_curso}"

#### Modelos para la Gestión Administrativa ####

# Horario model
class Horario(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=9, choices=[
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.curso.nombre_curso} - {self.dia_semana} {self.hora_inicio}-{self.hora_fin}"

# Pago model
class Pago(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido')
    ]
    TIPO_PAGO_CHOICES = [
        ('matricula', 'Matrícula'),
        ('pension', 'Pensión'),
        ('otros', 'Otros')
    ]
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=50, choices=TIPO_PAGO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    fecha_pago = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"Pago de {self.estudiante.nombres} {self.estudiante.apellidos} - {self.tipo_pago}"