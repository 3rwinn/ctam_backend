from rest_framework import serializers
from .models import Mission, Palier, TypeEntree, TypeSortie, Evenement, Communication, TimeLine

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = "__all__"

class PalierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palier
        fields = "__all__"

class TypeEntreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEntree
        fields = "__all__"
        
class TypeSortieSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSortie
        fields = "__all__"


class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = "__all__"


class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = "__all__"

class TimeLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLine
        fields = "__all__"