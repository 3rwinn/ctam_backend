from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, generics

from .serializers import EngagementSerializer, Engagement, MouvementSerializer, Mouvement, DepenseSerializer, Depense
from .helpers import get_engagement_stats, get_engagement_stats_by_mission
from django.db.models import Sum


class EngagementList(generics.ListCreateAPIView):
    """
    Créer un engagement ou recuperer tous les engagements
    """

    queryset = Engagement.objects.all()
    serializer_class = EngagementSerializer
    permission_classes = [permissions.IsAuthenticated]


class EngagementDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier un engagement
    """

    queryset = Engagement.objects.all()
    serializer_class = EngagementSerializer
    permission_classes = [permissions.IsAuthenticated]


class MouvementList(generics.ListCreateAPIView):
    """
    Créer un mouvement ou recuperer tous les mouvements
    """

    queryset = Mouvement.objects.all()
    serializer_class = MouvementSerializer
    permission_classes = [permissions.IsAuthenticated]


class MouvementDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier un mouvement
    """

    queryset = Mouvement.objects.all()
    serializer_class = MouvementSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepenseList(generics.ListCreateAPIView):
    """
    Créer une depense ou recuperer toutes les depenses
    """

    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepenseDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier une depense
    """

    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def engagement_entree_by_date(request, start_date, end_date):
    if request.method == 'GET':
        all_entrees = Mouvement.objects.all()
        total_all_entree_query = all_entrees.aggregate(
            montant=Sum('montant'))
        total_all_entree = total_all_entree_query['montant'] if total_all_entree_query else 0

        entrees_by_date = Mouvement.objects.filter(
            date__range=[start_date, end_date])
        total_entree_by_date_query = entrees_by_date.aggregate(
            montant=Sum('montant'))
        total_entree_by_date = total_entree_by_date_query['montant'] if total_entree_by_date_query else 0

        return Response({
            'total_entree': total_all_entree,
            'total_entree_by_date': total_entree_by_date,
            'entrees_by_date': MouvementSerializer(entrees_by_date, many=True).data
        }, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def engagement_depense_by_date(request, start_date, end_date):
    if request.method == 'GET':
        all_depenses = Depense.objects.all()
        total_all_depense_query = all_depenses.aggregate(
            montant=Sum('montant'))
        total_all_depense = total_all_depense_query['montant'] if total_all_depense_query else 0

        depenses_by_date = Depense.objects.filter(
            date__range=[start_date, end_date])
        total_depense_by_date_query = depenses_by_date.aggregate(
            montant=Sum('montant'))
        total_depense_by_date = total_depense_by_date_query['montant'] if total_depense_by_date_query else 0

        return Response({
            'total_depense': total_all_depense,
            'total_depense_by_date': total_depense_by_date,
            'depenses_by_date': DepenseSerializer(depenses_by_date, many=True).data
        }, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



# API to return data from get_engagements_stats function in the helpers.py file
@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def engagements_stats(request):
    """
    Récuperer les statistiques des engagements
    """
    if request.method == 'GET':
        engagements_stats = get_engagement_stats()
        return Response(engagements_stats, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def engagements_stats_by_mission(request, mission):
    """
    Récuperer les statistiques des engagements par mission
    """
    if request.method == 'GET':
        engagements_stats = get_engagement_stats_by_mission(
            remote_mission=mission)
        return Response(engagements_stats, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
