from .models import EntreeCaisse, SortieCaisse, SuiviBanque, FicheDimanche
from common.models import Mission, TypeEntree
from django.db.models import Sum, Count
from datetime import datetime
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear, ExtractWeek, ExtractWeekDay, Extract


def get_finances_stats(mission, date_debut, date_fin):

    entree_offrande = EntreeCaisse.objects.filter(type_entree__libelle='Offrande', date__range=[
                                                  date_debut, date_fin], mission__id=mission).aggregate(Sum('montant'))['montant__sum']

    entree_dime = EntreeCaisse.objects.filter(type_entree__libelle='Dîme', date__range=[
                                              date_debut, date_fin], mission__id=mission).aggregate(Sum('montant'))['montant__sum']

    total_entree_offrande = entree_offrande if entree_offrande is not None else 0
    total_entree_dime = entree_dime if entree_dime is not None else 0

    sortie_from_date_range = SortieCaisse.objects.filter(date__range=[
        date_debut, date_fin], mission__id=mission).aggregate(Sum('montant'))[
        'montant__sum']

    total_sortie = sortie_from_date_range if sortie_from_date_range is not None else 0

    total_entree = total_entree_offrande + total_entree_dime

    suivi_banque_versement = SuiviBanque.objects.filter(action="versement",
                                                        date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']

    suivi_banque_retrait = SuiviBanque.objects.filter(
        action='retrait', date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']

    total_suivi_banque_versement = suivi_banque_versement if suivi_banque_versement is not None else 0

    total_suivi_banque_retrait = suivi_banque_retrait if suivi_banque_retrait is not None else 0

    calcul_solde_caisse = (total_entree - total_sortie) - \
        total_suivi_banque_versement

    solde_caisse = calcul_solde_caisse if calcul_solde_caisse > 0 else 0

    solde_banque = total_suivi_banque_versement - total_suivi_banque_retrait

    # Entree & Depense by month based on the date range
    entree_by_month = EntreeCaisse.objects.filter(date__range=[date_debut, date_fin], mission__id=mission).values('date__month').annotate(
        entree_sum=Sum('montant')).order_by('date__month')
    
    sortie_by_month = SortieCaisse.objects.filter(date__range=[date_debut, date_fin], mission__id=mission).values('date__month').annotate(
        sortie_sum=Sum('montant')).order_by('date__month')    

    # Entree offrande & dime by month based on the last 6 month
    entree_offrande_for_last_6_month = EntreeCaisse.objects.filter(type_entree__libelle='Offrande', mission__id=mission).values('date__month').annotate(
        entree_sum=Sum('montant')).order_by('date__month')[:6]

    entree_dime_for_last_6_month = EntreeCaisse.objects.filter(type_entree__libelle='Dîme', mission__id=mission).values('date__month').annotate(
        entree_sum=Sum('montant')).order_by('date__month')[:6]

    # Entree offrande & dime & depense variation by month based on the last 2 month
    current_month = datetime.now()

    entree_offrande_for_last_2_month = EntreeCaisse.objects.filter(type_entree__libelle='Offrande', date__month__lt=current_month.month, mission__id=mission).values('date__month').annotate(
        entree_sum=Sum('montant')).order_by('date__month')[:2]

    entree_dime_for_last_2_month = EntreeCaisse.objects.filter(type_entree__libelle='Dîme', date__month__lt=current_month.month, mission__id=mission).values('date__month').annotate(
        entree_sum=Sum('montant')).order_by('date__month')[:2]

    depense_for_last_2_month = SortieCaisse.objects.filter(date__month__lt=current_month.month, mission__id=mission).values('date__month').annotate(
        depense_sum=Sum('montant')).order_by('date__month')[:2]

    return {
        'total_entree_offrande': total_entree_offrande,
        'total_entree_dime': total_entree_dime,
        'total_depense': total_sortie,
        'solde_caisse': solde_caisse,
        'solde_banque': solde_banque,
        'entree_by_month': entree_by_month,
        'sortie_by_month': sortie_by_month,
        'entree_offrande_for_last_6_month': entree_offrande_for_last_6_month,
        'entree_dime_for_last_6_month': entree_dime_for_last_6_month,
        'entree_offrande_for_last_2_month': entree_offrande_for_last_2_month,
        'entree_dime_for_last_2_month': entree_dime_for_last_2_month,
        'depense_for_last_2_month': depense_for_last_2_month,
    }
