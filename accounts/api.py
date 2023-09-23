from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .models import UserMission
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, UpdateUserSerializer, UserMissionSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from common.models import Mission

# Login API


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user_mission = UserMission.objects.filter(user=user.id).last()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
            "mission": {
                "id": user_mission.mission.id if user_mission else 0,
                "libelle": user_mission.mission.libelle if user_mission else "all",
            }
        })



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # check if mission exist from request
        if request.data["mission"]:
            # get user from request
            user = User.objects.get(email=request.data["email"])
            # get mission from request
            mission = Mission.objects.get(id=request.data["mission"])
            # create userMission
            userMission = UserMission(user=user, mission=mission)
            # save userMission
            userMission.save()

        # return Response({
        #   "user": UserSerializer(user, context=self.get_serializer_context()).data,
        #   "token": AuthToken.objects.create(user)[1]
        # })
        return Response({
            "success": True,
            "message": "Utilisateur créé avec succès, vous pouvez maintenant vous connectez!"
        })

# Get User API


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user



class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        user.delete()
        return Response({
            "success": True,
            "message": "Utilisateur supprimé avec succès!"
        })


class UserMissionList(generics.ListCreateAPIView):
    """
    Créer une mission ou recuperer toutes les missions
    """

    queryset = UserMission.objects.all()
    serializer_class = UserMissionSerializer


class UserMissionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Récuperer ou modifier une mission
    """

    queryset = UserMission.objects.all()
    serializer_class = UserMissionSerializer


# API to update user info and password
class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = UpdateUserSerializer
        model = User
        # permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj_id = self.request.data['user_id']
            obj = self.model.objects.get(id=obj_id)
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Mauvais mot de passe."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Mot de passe mis à jour avec succès',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)