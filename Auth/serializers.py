from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Auth.models import Person


class PersonWriteSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=100, required=True)
    username = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Person
        fields = '__all__'

    def validate(self, attrs):
        if Person.objects.filter(username=attrs.get('username')).exists():
            raise ValidationError({'username': 'This username already exists', 'status': 0})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')

        person = Person.objects.create(**validated_data)

        person.set_password(password)
        person.is_active = True
        person.save()
        return person


class PersonReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'auth_token', 'full_name', 'username')

