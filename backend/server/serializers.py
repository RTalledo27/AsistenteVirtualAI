# serializers.py
from rest_framework import serializers
from .models import Estudiante, Facultad, Carrera, PlanEstudio, Curso, Matricula, HistorialAcademico, RequisitosPrevios, PlanEstudioCurso

class EstudiantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'  # or specify fields as a list

class FacultadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = '__all__'

class CarrerasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = '__all__'

class PlanEstudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanEstudio
        fields = '__all__'

class CursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class MatriculasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'

class HistorialAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialAcademico
        fields = '__all__'

class RequisitosPreviosSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisitosPrevios
        fields = '__all__'

class PlanEstudioCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanEstudioCurso
        fields = '__all__'