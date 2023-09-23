from .models import Engagement, Mouvement, Depense
from common.models import Mission, Palier
from membres.models import Membre
from django.db.models import Sum, Count


def get_engagement_stats():

    members_count = Membre.objects.all().count()
    engagement_allcount = Engagement.objects.all().count()

    # django function to get the sum of palier montant for all engagements
    engagement_sum = Engagement.objects.all().aggregate(Sum('palier__montant'))['palier__montant__sum']
    # django function to get the sum of montant for all mouvements
    mouvement_allsum = Mouvement.objects.all().aggregate(Sum('montant'))['montant__sum']
    # django function to get the sum of montant for all depenses
    depense_sum = Depense.objects.all().aggregate(Sum('montant'))['montant__sum']
    # function to calculate the difference between engagement_sum and mouvement_sum
    
    real_engagement_sum = engagement_sum if engagement_sum is not None else 0
    real_mouvement_allsum = mouvement_allsum if mouvement_allsum is not None else 0
    
    
    restant = real_engagement_sum - real_mouvement_allsum
 
    # function to get the % of mouvement_sum from engagement_sum
    mouvement_percent = real_mouvement_allsum / real_engagement_sum * 100 if real_engagement_sum else 0
    # function to get the % of restant from engagement_sum
    restant_percent = restant / real_engagement_sum * 100 if real_engagement_sum else 100

    # django function to group engagement by palier, and get the sum of all engagement related to each palier, and the sum of all mouvement related to each palier, and count the number of engagement related to each palier
    # return also palier montant for each palier
    engagement_by_palier = Engagement.objects.values('palier__montant', 'palier__id').annotate(
        engagement_sum=Sum('palier__montant')).order_by('-engagement_sum')
    
    # loop through each palier in engagement_by_palier

    for palier in engagement_by_palier:
        # get the sum of montant for all mouvements related to each palier
        mouvement_sum = Mouvement.objects.filter(engagement__palier__id=palier['palier__id']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the palier dict
        palier['mouvement_sum'] = mouvement_sum
        # get the number of engagement related to each palier
        engagement_count = Engagement.objects.filter(palier__id=palier['palier__id']).count()
        # add the number of engagement to the palier dict
        palier['engagement_count'] = engagement_count


    # django function to group engagement by mission, and get the sum of all engagement related to each mission, and the sum of all mouvement related to each mission, and count the number of engagement related to each mission
    # return also mission libelle for each mission
    engagement_by_mission = Engagement.objects.values('mission__libelle', 'mission__id').annotate(
        engagement_sum=Sum('palier__montant')).order_by('-engagement_sum')
    
    # loop through each mission in engagement_by_mission

    for mission in engagement_by_mission:
        # get the sum of montant for all mouvements related to each mission
        mouvement_sum = Mouvement.objects.filter(engagement__mission__id=mission['mission__id']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the mission dict
        mission['mouvement_sum'] = mouvement_sum
        # get the number of engagement related to each mission
        engagement_count = Engagement.objects.filter(mission__id=mission['mission__id']).count()
        # add the number of engagement to the mission dict
        mission['engagement_count'] = engagement_count

    # django function to group engagement by membre, and get the sum of all engagement related to each membre, and the sum of all mouvement related to each membre, and count the number of engagement related to each membre
    # return also membre nom for each membre
    engagement_global_by_membre = Engagement.objects.values('membre__nom', 'membre__id').annotate(
        engagement_sum=Sum('palier__montant')).order_by('-engagement_sum')
    
    # loop through each membre in engagement_by_membre

    for membre in engagement_global_by_membre:
        # get the sum of montant for all mouvements related to each membre
        mouvement_sum_membre = Mouvement.objects.filter(engagement__membre__id=membre['membre__id']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the membre dict
        membre['mouvement_sum'] = mouvement_sum_membre
        # get the number of engagement related to each membre
        engagement_count_membre = Engagement.objects.filter(membre__id=membre['membre__id']).count()
        # add the number of engagement to the membre dict
        membre['engagement_count'] = engagement_count_membre
   
    # django function to get all engagement of a membre and for each engagement get the id, the mission libelle, the palier montant, the mouvement sum, the mouvement percent, the restant percent
    engagement_by_membre = Engagement.objects.values('id', 'mission__libelle', 'mission__id', 'palier__montant', 'membre__id', 'membre__nom', 'membre__prenom', 'membre__fonction', 'membre__contact', 'annee__year').annotate(
        mouvement_sum=Sum('mouvement__montant')).order_by('-palier__montant')
    
    # loop through each engagement in engagement_by_membre

    for engagement in engagement_by_membre:
        # get the sum of montant for all mouvements related to each engagement
        mouvement_sum_membre = Mouvement.objects.filter(engagement__id=engagement['id']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the engagement dict
        engagement['mouvement_sum'] = mouvement_sum_membre if mouvement_sum_membre else 0
        # get the % of mouvement_sum from palier montant
        mouvement_percent_membre = mouvement_sum_membre / engagement['palier__montant'] * 100 if mouvement_sum_membre else 0
        # add the % of mouvement_sum to the engagement dict
        engagement['mouvement_percent'] = mouvement_percent_membre
        # get the % of restant from palier montant
        restant_percent_membre = (engagement['palier__montant'] - mouvement_sum_membre) / engagement['palier__montant'] * 100 if mouvement_sum_membre else 100
        # add the % of restant to the engagement dict
        engagement['restant_percent'] = restant_percent_membre

    
    # django function to group mouvement by day and get the sum of all mouvement related to each day and calculate the restant for each day
    mouvement_by_day = Mouvement.objects.values('date').annotate(
        mouvement_sum=Sum('montant')).order_by('date')
    
    # loop through each mouvement in mouvement_by_day

    for mouvement in mouvement_by_day:
        # get the sum of montant for all mouvements related to each day
        mouvement_sum_day = Mouvement.objects.filter(date=mouvement['date']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the mouvement dict
        mouvement['mouvement_sum'] = mouvement_sum_day
        # calculate the restant for each day
        restant_day = engagement_sum - mouvement_sum_day
        # add the restant to the mouvement dict
        mouvement['restant'] = restant_day

    # django function to group mouvement by month and get the sum of all mouvement related to each month and calculate the restant for each month
    mouvement_by_month = Mouvement.objects.values('date__month').annotate(
        mouvement_sum=Sum('montant')).order_by('date__month')
    
    # loop through each mouvement in mouvement_by_month

    for mouvement in mouvement_by_month:
        # get the sum of montant for all mouvements related to each month
        mouvement_sum_month = Mouvement.objects.filter(date__month=mouvement['date__month']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the mouvement dict
        mouvement['mouvement_sum'] = mouvement_sum_month
        # calculate the restant for each month
        restant_month = engagement_sum - mouvement_sum_month
        # add the restant to the mouvement dict
        mouvement['restant'] = restant_month

    
    # return all the variables in a dictionary
    return {
        'members_count': members_count,
        'engagement_count': engagement_allcount,
        'engagement_sum': engagement_sum,
        'mouvement_sum': mouvement_allsum,
        'depense_sum': depense_sum,
        'restant': restant,
        'mouvement_percent': mouvement_percent,
        'restant_percent': restant_percent,
        'engagement_by_palier': engagement_by_palier,
        'engagement_by_mission': engagement_by_mission,
        'engagement_global_by_membre': engagement_global_by_membre,
        'engagement_by_membre': engagement_by_membre,
        'mouvement_by_day': mouvement_by_day,
        'mouvement_by_month': mouvement_by_month,
    }




def get_engagement_stats_by_mission(remote_mission):

    members_count = Membre.objects.filter(mission_id=remote_mission).count()
    engagement_allcount = Engagement.objects.filter(mission_id=remote_mission).count()

    # django function to get the sum of palier montant for all engagements
    engagement_sum = Engagement.objects.filter(mission_id=remote_mission).aggregate(Sum('palier__montant'))['palier__montant__sum']
    # django function to get the sum of montant for all mouvements
    mouvement_allsum = Mouvement.objects.filter(engagement__mission__id=remote_mission).aggregate(Sum('montant'))['montant__sum']
    # django function to get the sum of montant for all depenses
    depense_sum = Depense.objects.filter(mission_id=remote_mission).aggregate(Sum('montant'))['montant__sum']
    # function to calculate the difference between engagement_sum and mouvement_sum
    
    real_engagement_sum = engagement_sum if engagement_sum is not None else 0
    real_mouvement_allsum = mouvement_allsum if mouvement_allsum is not None else 0
    
    
    restant = real_engagement_sum - real_mouvement_allsum
 
    # function to get the % of mouvement_sum from engagement_sum
    mouvement_percent = real_mouvement_allsum / real_engagement_sum * 100 if real_engagement_sum else 0
    # function to get the % of restant from engagement_sum
    restant_percent = restant / real_engagement_sum * 100 if real_engagement_sum else 100

    # django function to group engagement by palier, and get the sum of all engagement related to each palier, and the sum of all mouvement related to each palier, and count the number of engagement related to each palier
    # return also palier montant for each palier
    engagement_by_palier = Engagement.objects.filter(mission_id=remote_mission).values('palier__montant', 'palier__id').annotate(
        engagement_sum=Sum('palier__montant')).order_by('-engagement_sum')
    
    # loop through each palier in engagement_by_palier

    for palier in engagement_by_palier:
        # get the sum of montant for all mouvements related to each palier
        mouvement_sum = Mouvement.objects.filter(engagement__palier__id=palier['palier__id']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the palier dict
        palier['mouvement_sum'] = mouvement_sum
        # get the number of engagement related to each palier
        engagement_count = Engagement.objects.filter(palier__id=palier['palier__id']).count()
        # add the number of engagement to the palier dict
        palier['engagement_count'] = engagement_count


    # django function to group engagement by mission, and get the sum of all engagement related to each mission, and the sum of all mouvement related to each mission, and count the number of engagement related to each mission
    # return also mission libelle for each mission
    engagement_by_mission = Engagement.objects.values('mission__libelle', 'mission__id').annotate(
        engagement_sum=Sum('palier__montant')).order_by('-engagement_sum')
    
    # loop through each mission in engagement_by_mission

    for mission in engagement_by_mission:
        # get the sum of montant for all mouvements related to each mission
        mouvement_sum = Mouvement.objects.filter(engagement__mission__id=mission['mission__id']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the mission dict
        mission['mouvement_sum'] = mouvement_sum
        # get the number of engagement related to each mission
        engagement_count = Engagement.objects.filter(mission__id=mission['mission__id']).count()
        # add the number of engagement to the mission dict
        mission['engagement_count'] = engagement_count

    # django function to group engagement by membre, and get the sum of all engagement related to each membre, and the sum of all mouvement related to each membre, and count the number of engagement related to each membre
    # return also membre nom for each membre
    # engagement_global_by_membre = Engagement.objects.filter(mission__id=mission).values('membre__nom', 'membre__id').annotate(
    engagement_global_by_membre = Engagement.objects.values('membre__nom', 'membre__id').annotate(
        engagement_sum=Sum('palier__montant')).order_by('-engagement_sum')
    
    # loop through each membre in engagement_by_membre

    for membre in engagement_global_by_membre:
        # get the sum of montant for all mouvements related to each membre
        mouvement_sum_membre = Mouvement.objects.filter(engagement__membre__id=membre['membre__id']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the membre dict
        membre['mouvement_sum'] = mouvement_sum_membre
        # get the number of engagement related to each membre
        engagement_count_membre = Engagement.objects.filter(membre__id=membre['membre__id']).count()
        # add the number of engagement to the membre dict
        membre['engagement_count'] = engagement_count_membre
   
    # django function to get all engagement of a membre and for each engagement get the id, the mission libelle, the palier montant, the mouvement sum, the mouvement percent, the restant percent
    engagement_by_membre = Engagement.objects.values('id', 'mission__libelle', 'mission__id', 'palier__montant', 'membre__id', 'membre__nom', 'membre__prenom', 'membre__fonction', 'membre__contact', 'annee__year').annotate(
        mouvement_sum=Sum('mouvement__montant')).order_by('-palier__montant')
    
    # loop through each engagement in engagement_by_membre

    for engagement in engagement_by_membre:
        # get the sum of montant for all mouvements related to each engagement
        mouvement_sum_membre = Mouvement.objects.filter(engagement__id=engagement['id']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the engagement dict
        engagement['mouvement_sum'] = mouvement_sum_membre if mouvement_sum_membre else 0
        # get the % of mouvement_sum from palier montant
        mouvement_percent_membre = mouvement_sum_membre / engagement['palier__montant'] * 100 if mouvement_sum_membre else 0
        # add the % of mouvement_sum to the engagement dict
        engagement['mouvement_percent'] = mouvement_percent_membre
        # get the % of restant from palier montant
        restant_percent_membre = (engagement['palier__montant'] - mouvement_sum_membre) / engagement['palier__montant'] * 100 if mouvement_sum_membre else 100
        # add the % of restant to the engagement dict
        engagement['restant_percent'] = restant_percent_membre

    
    # django function to group mouvement by day and get the sum of all mouvement related to each day and calculate the restant for each day
    mouvement_by_day = Mouvement.objects.filter(engagement__mission__id=remote_mission).values('date').annotate(
        mouvement_sum=Sum('montant')).order_by('date')
    
    # loop through each mouvement in mouvement_by_day

    for mouvement in mouvement_by_day:
        # get the sum of montant for all mouvements related to each day
        mouvement_sum_day = Mouvement.objects.filter(date=mouvement['date']).aggregate(Sum('montant'))['montant__sum']
        # add the sum of mouvement to the mouvement dict
        mouvement['mouvement_sum'] = mouvement_sum_day
        # calculate the restant for each day
        restant_day = engagement_sum - mouvement_sum_day
        # add the restant to the mouvement dict
        mouvement['restant'] = restant_day

    
    # return all the variables in a dictionary
    return {
        'members_count': members_count,
        'engagement_count': engagement_allcount,
        'engagement_sum': engagement_sum,
        'mouvement_sum': mouvement_allsum,
        'depense_sum': depense_sum,
        'restant': restant,
        'mouvement_percent': mouvement_percent,
        'restant_percent': restant_percent,
        'engagement_by_palier': engagement_by_palier,
        'engagement_by_mission': engagement_by_mission,
        'engagement_global_by_membre': engagement_global_by_membre,
        'engagement_by_membre': engagement_by_membre,
        'mouvement_by_day': mouvement_by_day,
    }


