from rest_framework import serializers
from .models import Membre


class MembreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = "__all__"


class UploadMembreSerializer(serializers.Serializer):
    fichier = serializers.FileField()
    mission = serializers.CharField()
    mode = serializers.CharField()
