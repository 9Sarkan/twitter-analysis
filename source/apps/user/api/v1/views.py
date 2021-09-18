import random
from email import message

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import status, views
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.transaction import atomic
from .serializers import *
from django.shortcuts import Http404
from .permissions import RegisterPermission
from base.redis import Redis


@api_view(["POST"])
def forget_password_get_code(request):
    """ """
    email = request.data.get("email")
    if not email:
        return Response(
            {"errors": [{"code": 400, "message": _("email field required!")}]},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = User.objects.filter(email=email)
    if not user.exists():
        return Response(
            {
                "errors": [
                    {
                        "code": 400,
                        "message": _(
                            "This email does not exists in system you can signup!"
                        ),
                    }
                ]
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = user.first()
    code = random.randint(10000, 99999)
    Redis().set_token(user.username, code)
    user.email_user(
        subject="Password Reset",
        message=f"your password reset code is: {settings.RESET_PASSWORD_URL % (user.id, code)}",
    )
    return Response(
        {"code": 200, "message": _("Password reset code sent to your email!")}
    )


@api_view(["POST"])
def reset_password(request, user_id, token):
    """ """
    # validate user_id
    user = User.objects.filter(id=user_id)
    if not user.exists():
        raise Http404
    user = user.first()

    # validate token
    code = Redis().get_token(user.username)

    if code != token:
        raise Http404

    # validate password
    password = request.data.get("password")
    try:
        validate_password(password, user)
    except ValidationError as e:
        body = []
        for i in e.messages:
            body.append({"code": 400, "message": i})
        return Response(
            {"errors": body},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(password)
    user.save()
    return Response({"code": 200, "message": _("Your password successfully changed!")})


class UserViewSet(ModelViewSet):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (RegisterPermission,)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
