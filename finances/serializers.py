from rest_framework import serializers
from .models import EntreeCaisse, SortieCaisse, SuiviBanque, FicheDimanche

class EntreeCaisseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntreeCaisse
        fields = "__all__"

class SortieCaisseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortieCaisse
        fields = "__all__"


class SuiviBanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviBanque
        fields = "__all__"


class FicheDimancheSerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheDimanche
        fields = "__all__"