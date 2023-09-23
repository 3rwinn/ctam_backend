from django.urls import path, include
from .api import EntreeCaisseList, EntreeCaisseDetail, SortieCaisseList, SortieCaisseDetail, SuiviBanqueList, SuiviBanqueDetail, FicheDimancheList, FicheDimancheDetail, finances_stats, entree_caisse_by_date, sortie_caisse_by_date, suivi_banque_by_date

urlpatterns = [
    path('entrees', EntreeCaisseList.as_view(), name="get_post_entrees"),
    path('entree/<int:pk>', EntreeCaisseDetail.as_view(),
         name="get_update_delete_entree"),
    path('sorties', SortieCaisseList.as_view(), name="get_post_sorties"),
    path('sortie/<int:pk>', SortieCaisseDetail.as_view(),
         name="get_update_delete_sortie"),
    path('suivis', SuiviBanqueList.as_view(), name="get_post_suivis"),
    path('suivi/<int:pk>', SuiviBanqueDetail.as_view(),
         name="get_update_delete_suivi"),
    path('fiches', FicheDimancheList.as_view(), name="get_post_fiches"),
    path('fiche/<int:pk>', FicheDimancheDetail.as_view(),
         name="get_update_delete_fiche"),
    path('stats/mission/<int:mission>/debut/<str:date_debut>/fin/<str:date_fin>',
         finances_stats, name='finances_stats'),
    path('entrees/date/<str:start_date>/<str:end_date>', entree_caisse_by_date,
         name="get_entrees_by_date"),
    path('sorties/date/<str:start_date>/<str:end_date>', sortie_caisse_by_date,
         name="get_sorties_by_date"),
    path('suivis/date/<str:start_date>/<str:end_date>', suivi_banque_by_date,
         name="get_suivis_by_date"),

]
