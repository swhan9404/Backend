from rest_framework import serializers

from .models import Person, Concept, Death


class ConceptSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Concept
        fields = "__all__"

class PersonSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Person
        fields = "__all__"

class DeathSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Death
        fields = "__all__"