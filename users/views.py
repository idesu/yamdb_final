from django.core.mail import send_mail
from django.http import JsonResponse
from django_filters import rest_framework
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from vcode import digits as generate_code

from .models import User
from .permissions import AdminOnly
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, AdminOnly]
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_fields = ['username', ]

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        else:
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_mail(request):
    if request.method == 'POST':
        try:
            email = request.data.get('email')
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "No user found with the given email."}, status=400)
        confirmation_code = generate_code(ndigits=6)
        serializer = CustomUserSerializer(
            user, data={'confirmation_code': confirmation_code}, partial=True)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                'Подтверждение регистрации Yamdb',
                f'confirmation_code: {confirmation_code}',
                'Yamdb.ru <admin@yamdb.ru>',
                [email],
                fail_silently=False
            )
            return Response(serializer.data)
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_token(request):
    if request.method == 'POST':
        try:
            confirmation_code = request.data.get('confirmation_code')
            email = request.data.get('email')
            user = User.objects.get(
                email=email, confirmation_code=confirmation_code)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "No user found with the given credentials. "
                          "Your request must provide json with valid email and confirmation_code fields"},
                status=400
            )
        refresh = RefreshToken.for_user(user)
# Обновим код, чтобы избежать его повторного использования
        new_confirmation_code = generate_code(ndigits=6)
        serializer = CustomUserSerializer(
            user, data={'confirmation_code': new_confirmation_code}, partial=True)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({'refresh': str(refresh),
                             'access': str(refresh.access_token)})
