from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, generics

from .serializers import MissionSerializer, PalierSerializer, TypeEntreeSerializer, TypeSortieSerializer, EvenementSerializer, CommunicationSerializer, TimeLineSerializer
from .models import Mission, Palier, TypeEntree, TypeSortie, Evenement, Communication, TimeLine

import http.client
import json


class MissionList(generics.ListCreateAPIView):
    """
    Créer une mission ou recuperer toutes les missions
    """

    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class MissionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier une mission
    """

    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PalierList(generics.ListCreateAPIView):
    """
    Créer un palier ou recuperer toutes les paliers
    """

    queryset = Palier.objects.all()
    serializer_class = PalierSerializer
    permission_classes = [permissions.IsAuthenticated]


class PalierDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier un palier
    """

    queryset = Palier.objects.all()
    serializer_class = PalierSerializer
    permission_classes = [permissions.IsAuthenticated]


class TypeEntreeList(generics.ListCreateAPIView):
    """
    Créer un typeEntree ou recuperer toutes les typeEntrees
    """

    queryset = TypeEntree.objects.all()
    serializer_class = TypeEntreeSerializer
    permission_classes = [permissions.IsAuthenticated]


class TypeEntreeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier un typeEntree
    """

    queryset = TypeEntree.objects.all()
    serializer_class = TypeEntreeSerializer
    permission_classes = [permissions.IsAuthenticated]


class TypeSortieList(generics.ListCreateAPIView):
    """
    Créer un typeSortie ou recuperer toutes les typeSorties
    """

    queryset = TypeSortie.objects.all()
    serializer_class = TypeSortieSerializer
    permission_classes = [permissions.IsAuthenticated]


class TypeSortieDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier un typeSortie
    """

    queryset = TypeSortie.objects.all()
    serializer_class = TypeSortieSerializer
    permission_classes = [permissions.IsAuthenticated]


class EvenementList(generics.ListCreateAPIView):
    """
    Créer un evenement ou recuperer tous les evenements
    """

    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [permissions.IsAuthenticated]


class EvenementDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier un evenement
    """

    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommunicationList(generics.ListCreateAPIView):
    """
    Créer une communication ou recuperer toutes les communications
    """

    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommunicationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier une communication
    """

    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class TimeLineList(generics.ListCreateAPIView):
    """
    Créer une timeLine ou recuperer toutes les timeLines
    """

    queryset = TimeLine.objects.all()
    serializer_class = TimeLineSerializer
    permission_classes = [permissions.IsAuthenticated]


class TimeLineDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier une timeLine
    """

    queryset = TimeLine.objects.all()
    serializer_class = TimeLineSerializer
    permission_classes = [permissions.IsAuthenticated]


# Write an api that will take a stringified array of phone numbers and a message, parse the array into a dictionnary look through it

@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def send_sms(request):
    BASE_URL = "gy6dv8.api.infobip.com"
    API_KEY = "App 5e11c97b18c80912f87ee238c12e30c0-aafd5c7a-ab08-4a8b-82ed-ffd594c1522b"

    SENDER = "MISSION ADS"

    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    if request.method == 'POST':
        # get the phone numbers and message from the request
        recipients = request.data['recipients']
        message = request.data['message']
        # parse the phone numbers into a list
        print(f"message: {message}")
        try:
            # format the message so that it supports unicode characters
            message = message.encode('utf-8').decode('unicode-escape')
            phone_numbers = json.loads(recipients)
        except json.decoder.JSONDecodeError:
            return Response({"error": "malformed json"}, status=status.HTTP_400_BAD_REQUEST)

        for number in phone_numbers:
            # print("type " + type(number))
            print("sending sms to " + number)
            conn = http.client.HTTPSConnection(BASE_URL)
            payload1 = "{\"messages\":" \
                "[{\"from\":\"" + SENDER + "\"" \
                ",\"destinations\":" \
                "[{\"to\":\"" + number + "\"}]," \
                "\"text\":\"" + message + "\"}]}"

            conn.request("POST", "/sms/2/text/advanced", payload1, headers)

            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
        return Response(data, status=status.HTTP_200_OK)
        # return Response({"ok": "ok"}, status=status.HTTP_200_OK)

    return Response("Method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
