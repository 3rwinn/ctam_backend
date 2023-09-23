from django.urls import path, include
from .api import MissionList, MissionDetail, PalierList, PalierDetail, TypeSortieList, TypeSortieDetail, TypeEntreeList, TypeEntreeDetail, EvenementList, EvenementDetail, CommunicationList, CommunicationDetail, TimeLineList, TimeLineDetail, send_sms

urlpatterns = [
    path('missions', MissionList.as_view(), name="get_post_missions"),
    path('mission/<int:pk>', MissionDetail.as_view(),
         name="get_update_delete_mission"),
    path('paliers', PalierList.as_view(), name="get_post_paliers"),
    path('palier/<int:pk>', PalierDetail.as_view(),
         name="get_update_delete_palier"),
    path('typeentrees', TypeEntreeList.as_view(), name="get_post_typeentrees"),
    path('typeentree/<int:pk>', TypeEntreeDetail.as_view(),
         name="get_update_delete_typeentree"),
    path('typesorties', TypeSortieList.as_view(), name="get_post_typeSorties"),
    path('typesortie/<int:pk>', TypeSortieDetail.as_view(),
         name="get_update_delete_typesortie"),
    path('evenements', EvenementList.as_view(), name="get_post_evenements"),
    path('evenement/<int:pk>', EvenementDetail.as_view(),
         name="get_update_delete_evenement"),
    path('communications', CommunicationList.as_view(),
         name="get_post_communications"),
    path('communication/<int:pk>', CommunicationDetail.as_view(),
         name="get_update_delete_communication"),
    path('timelines', TimeLineList.as_view(), name="get_post_timeline"),
    path('timeline/<int:pk>', TimeLineDetail.as_view(),
         name="get_update_delete_timeline"),
    path('sms', send_sms, name="send_sms"),

]
