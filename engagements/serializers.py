from rest_framework import serializers
from .models import Engagement, Mouvement, Depense

class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engagement
        fields = "__all__"


class MouvementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mouvement
        fields = "__all__"
 
class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = "__all__"