from django.shortcuts import render
import logging
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from user.serializer import (
    LoginSerializer,
    MyTokenObtainPairSerializer,
)

logging.basicConfig(
    format="%(levelname)s - %(asctime)s - %(message)s",
    level=logging.INFO,
)

# Create your views here.
class AuthenticationView(APIView):
    """Authenticates the user, if the credentials are valid
    the user gets an access front and an http only refresh token in the cookies.
    """

    def post(self, request, *args, **kwargs):

        #Check if the user credentials are valid
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)

            #Check if the user exists
            if user is not None:
                token = MyTokenObtainPairSerializer
                refresh = token.get_token(user)

                response = HttpResponse()

                json_response = JsonResponse({"access_token": str(refresh.access_token),
                                            "refresh_token": str(refresh)})
                response.status_code = json_response.status_code
                response.content = json_response.content
                response["content-type"] = json_response["content-type"]
                logging.info("Sikeres bejelentkezés.")

                return response

            return Response({"message": "Hibás felhasználónónév vagy jelszó.", "type":"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("asd")
        return Response({"message": serializer.errors, "type":"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

