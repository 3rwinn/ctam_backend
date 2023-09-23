from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, generics

from .serializers import EntreeCaisseSerializer, SortieCaisseSerializer, SuiviBanqueSerializer, FicheDimancheSerializer
from .models import EntreeCaisse, SortieCaisse, SuiviBanque, FicheDimanche

from .helpers import get_finances_stats
from django.db.models import Sum


class EntreeCaisseList(generics.ListCreateAPIView):
    """
    Créer une entreeCaisse ou recuperer toutes les entreeCaisses
    """

    queryset = EntreeCaisse.objects.all()
    serializer_class = EntreeCaisseSerializer
    permission_classes = [permissions.IsAuthenticated]


class EntreeCaisseDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier une entreeCaisse
    """

    queryset = EntreeCaisse.objects.all()
    serializer_class = EntreeCaisseSerializer
    permission_classes = [permissions.IsAuthenticated]


class SortieCaisseList(generics.ListCreateAPIView):
    """
    Créer une sortieCaisse ou recuperer toutes les sortieCaisses
    """

    queryset = SortieCaisse.objects.all()
    serializer_class = SortieCaisseSerializer
    permission_classes = [permissions.IsAuthenticated]


class SortieCaisseDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier une sortieCaisse
    """

    queryset = SortieCaisse.objects.all()
    serializer_class = SortieCaisseSerializer
    permission_classes = [permissions.IsAuthenticated]


class SuiviBanqueList(generics.ListCreateAPIView):
    """
    Créer un suiviBanque ou recuperer toutes les suiviBanques
    """

    queryset = SuiviBanque.objects.all()
    serializer_class = SuiviBanqueSerializer
    permission_classes = [permissions.IsAuthenticated]


class SuiviBanqueDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier un suiviBanque
    """

    queryset = SuiviBanque.objects.all()
    serializer_class = SuiviBanqueSerializer
    permission_classes = [permissions.IsAuthenticated]


class FicheDimancheList(generics.ListCreateAPIView):
    """
    Créer une ficheDimanche ou recuperer toutes les ficheDimanches
    """

    queryset = FicheDimanche.objects.all()
    serializer_class = FicheDimancheSerializer
    permission_classes = [permissions.IsAuthenticated]


class FicheDimancheDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier une ficheDimanche
    """

    queryset = FicheDimanche.objects.all()
    serializer_class = FicheDimancheSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def finances_stats(request, mission, date_debut, date_fin):
    if request.method == "GET":

        finances_stats = get_finances_stats(
            mission, date_debut=date_debut, date_fin=date_fin)
        return Response(finances_stats, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# django generic api view to get EntreeCaisse based on start_date and end_date
class EntreeCaisseByDateList(generics.ListAPIView):
    serializer_class = EntreeCaisseSerializer

    def get_queryset(self):
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
        return EntreeCaisse.objects.filter(date__range=[start_date, end_date])


@api_view(['GET'])
def entree_caisse_by_date(request, start_date, end_date):
    if request.method == "GET":
        all_entree_caisse = EntreeCaisse.objects.all()
        total_all_entree_caisse_query = all_entree_caisse.aggregate(Sum('montant'))[
            'montant__sum']
        
        total_all_entree_caisse = total_all_entree_caisse_query if total_all_entree_caisse_query else 0
        
        entree_caisse_by_date = EntreeCaisse.objects.filter(
            date__range=[start_date, end_date])
        total_entree_caisse_by_date_query = entree_caisse_by_date.aggregate(Sum('montant'))[
            'montant__sum']
        
        total_entree_caisse_by_date = total_entree_caisse_by_date_query if total_entree_caisse_by_date_query else 0

        return Response(
            {'total_entree_caisse_by_date': total_entree_caisse_by_date,
             'total_all_entree_caisse': total_all_entree_caisse,
             'entree_caisse_by_date': EntreeCaisseSerializer(entree_caisse_by_date, many=True).data},
            status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def sortie_caisse_by_date(request, start_date, end_date):

    if request.method == "GET":
        all_sortie_caisse = SortieCaisse.objects.all()
        total_all_sortie_caisse_query = all_sortie_caisse.aggregate(Sum('montant'))[
            'montant__sum']
        
        total_all_sortie_caisse = total_all_sortie_caisse_query if total_all_sortie_caisse_query else 0
        
        sortie_caisse_by_date = SortieCaisse.objects.filter(
            date__range=[start_date, end_date])
        total_sortie_caisse_by_date_query = sortie_caisse_by_date.aggregate(Sum('montant'))[
            'montant__sum']
        
        total_sortie_caisse_by_date = total_sortie_caisse_by_date_query if total_sortie_caisse_by_date_query else 0

        return Response(
            {'total_sortie_caisse_by_date': total_sortie_caisse_by_date,
             'total_all_sortie_caisse': total_all_sortie_caisse,
             'sortie_caisse_by_date': SortieCaisseSerializer(sortie_caisse_by_date, many=True).data},
            status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST) 
    

@api_view(['GET'])
def suivi_banque_by_date(request, start_date, end_date):
        if request.method == "GET":
            all_suivi_banque = SuiviBanque.objects.all()
            total_all_suivi_banque_query = all_suivi_banque.aggregate(Sum('montant'))[
                'montant__sum']
            
            total_all_suivi_banque = total_all_suivi_banque_query if total_all_suivi_banque_query else 0
            
            suivi_banque_by_date = SuiviBanque.objects.filter(
                date__range=[start_date, end_date])
            total_suivi_banque_by_date_query = suivi_banque_by_date.aggregate(Sum('montant'))[
                'montant__sum']
            
            total_suivi_banque_by_date = total_suivi_banque_by_date_query if total_suivi_banque_by_date_query else 0
    
            return Response(
                {'total_suivi_banque_by_date': total_suivi_banque_by_date,
                'total_all_suivi_banque': total_all_suivi_banque,
                'suivi_banque_by_date': SuiviBanqueSerializer(suivi_banque_by_date, many=True).data},
                status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# django generic api view to get SortieCaisse based on start_date and end_date
# class SortieCaisseByDateList(generics.ListAPIView):
#     serializer_class = SortieCaisseSerializer

#     def get_queryset(self):
#         start_date = self.kwargs['start_date']
#         end_date = self.kwargs['end_date']
#         return SortieCaisse.objects.filter(date__range=[start_date, end_date])

# django generic api view to get SuiviBanque based on start_date and end_date
# class SuiviBanqueByDateList(generics.ListAPIView):
#     serializer_class = SuiviBanqueSerializer

#     def get_queryset(self):
#         start_date = self.kwargs['start_date']
#         end_date = self.kwargs['end_date']
#         return SuiviBanque.objects.filter(date__range=[start_date, end_date])
