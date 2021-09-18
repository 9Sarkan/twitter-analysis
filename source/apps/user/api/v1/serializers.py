from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "last_name", "first_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data["password"])
            user.save()
        except KeyError:
            pass
        return user

    def validate(self, attrs):
        user = User(**attrs)
        # get the password from the attrs
        password = attrs.get("password")
        errors = dict()
        if password:
            try:
                # validate the password and catch the exception
                password_validation.validate_password(password=password, user=User)
            # the exception raised here is different than serializers.ValidationError
            except exceptions.ValidationError as e:
                errors["password"] = list(e.messages)
            if errors:
                raise serializers.ValidationError(errors)
        return super(UserSerializer, self).validate(attrs)
