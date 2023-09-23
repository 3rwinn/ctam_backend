from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, generics

from .serializers import MembreSerializer, UploadMembreSerializer
from .models import Membre
from common.models import Mission

from django.http import JsonResponse
import csv


class MembreList(generics.ListCreateAPIView):
    """
    Créer un membre ou recuperer toutes les membres
    """

    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    permission_classes = [permissions.IsAuthenticated]


class MembreDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier un membre
    """

    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    permission_classes = [permissions.IsAuthenticated]

class UploadMembreView(generics.CreateAPIView):
    serializer_class = UploadMembreSerializer
    # parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fichier = serializer.validated_data['fichier']
        mission = int(serializer.validated_data['mission'])
        mode = serializer.validated_data['mode']

        try:
            reader = csv.reader(fichier.read().decode(
                'iso-8859-1').splitlines(), delimiter=';')

            next(reader)  # skip header row if present

            for row in reader:
                # print(f"splitted {row[6]}")

                try:
                    selected_mission = Mission.objects.get(pk=mission)
                    # Create new membre
                    if mode == "nouveau":
                        Membre.objects.create(
                            mission = selected_mission,
                            nom = row[0],
                            prenom = row[1],
                            sexe = "homme" if row[2] == "m" else "femme",
                            fonction = row[3],
                            marie = True if row[4] == "oui" else False,
                            baptise = True if row[5] == "oui" else False,
                            contact = row[6],
                            habitation = row[7],
                            nouveau = True,
                            encadreur = row[8],
                            merged = False
                        )
                    else:
                        Membre.objects.create(
                            mission = selected_mission,
                            nom = row[0],
                            prenom = row[1],
                            sexe = "homme" if row[2] == "m" else "femme",
                            fonction = row[3],
                            marie = True if row[4] == "oui" else False,
                            baptise = True if row[5] == "oui" else False,
                            contact = row[6],
                            habitation = row[7],
                            nouveau = False,
                            encadreur = None,
                            merged = False
                        )

                except Mission.DoesNotExist:
                    return Response({'error': "Le mission choisie n'existe pas/plus"}, status=400)

        except Exception as e:
            return Response({'error': str(e)}, status=400)
        
        
        return Response({
                'message': 'Données enregistrées avec succès.'}, status=200)
