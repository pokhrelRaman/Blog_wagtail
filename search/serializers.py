from rest_framework import serializers

class TagSearchSerializer(serializers.Serializer):
    keywords = serializers.CharField(max_length = 200, required = True)
    tag = serializers.CharField(max_length = 200)
    category = serializers.CharField(max_length = 200)


class CategorySearchSerializer(serializers.Serializer):
    category = serializers.CharField(max_length = 200)

class KeywordsSearchSerializer(serializers.Serializer):
    keywords = serializers.CharField(max_length = 200, required = True)
