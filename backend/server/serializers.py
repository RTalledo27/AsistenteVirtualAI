 # serializers.py
from rest_framework import serializers
from .models import Estudiante, Facultad, Carrera, MallaCurricular, Curso, Matricula, HistorialAcademico, RequisitosPrevios

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

class MallaCurricularSerializer(serializers.ModelSerializer):
    class Meta:
        model = MallaCurricular
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
