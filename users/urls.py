from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet,
    get_confirmation_mail,
    reset_token
)

router_v1 = DefaultRouter()
router_v1.register(r'^users', CustomUserViewSet, basename="users_v1")

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/email/', get_confirmation_mail, name='send_confirmation_email'),
    path('v1/auth/token/', reset_token, name='token_obtain_pair'),
]
