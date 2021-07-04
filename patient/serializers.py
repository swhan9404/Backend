from rest_framework import serializers

from .models import Person, Death



class PersonSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Person
        fields = "__all__"

class DeathSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Death
        fields = "__all__"