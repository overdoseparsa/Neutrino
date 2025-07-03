
from rest_framework import serializers


class InputPostCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()

class PutPostSerializer(InputPostCreateSerializer):
    id = serializers.IntegerField()
