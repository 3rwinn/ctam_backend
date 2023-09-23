from django.urls import path, include
from .api import MembreList, MembreDetail, UploadMembreView

urlpatterns = [
    path("membres", MembreList.as_view(), name="get_post_membres"),
    path("membre/<int:pk>", MembreDetail.as_view(),
         name="get_update_delete_membres"),
     path("membre/upload", UploadMembreView.as_view(), name="upload_membre"),
]
