
from rest_framework import serializers


class InputPostCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()

class PutPostSerializer(InputPostCreateSerializer):
    id = serializers.IntegerField()

from .models import Post
class OutputPostSerailizer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta :
        model = Post
        fields = '__all__'

    def get_author(self, obj):
        return str(obj.author.username)