from django.urls import path, include
from .api import EngagementList, EngagementDetail, MouvementList, MouvementDetail, DepenseList, DepenseDetail, engagements_stats, engagements_stats_by_mission, engagement_entree_by_date, engagement_depense_by_date

urlpatterns = [
    path("overview", EngagementList.as_view(), name="get_post_engagements"),
    path("overview/<int:pk>", EngagementDetail.as_view(),
         name="get_update_delete_engagements"),
    path("mouvements", MouvementList.as_view(), name="get_post_mouvements"),
    path("mouvement/<int:pk>", MouvementDetail.as_view(),
         name="get_update_delete_mouvement"),
    path("depenses", DepenseList.as_view(), name="get_post_depenses"),
    path("depense/<int:pk>", DepenseDetail.as_view(),
         name="get_update_delete_depense"),
    path("stats", engagements_stats, name="engagement_stats"),
    path("stats/mission/<int:mission>", engagements_stats_by_mission,
         name="engagement_stats_by_mission"),
    path("entrees/date/<str:start_date>/<str:end_date>",
         engagement_entree_by_date, name="get_entrees_by_date"),
    path("depenses/date/<str:start_date>/<str:end_date>",
         engagement_depense_by_date, name="get_depenses_by_date"),
]
