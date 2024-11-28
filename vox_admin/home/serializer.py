from rest_framework import serializers

class ToolSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    status = serializers.ChoiceField(choices=["running", "stopped"])
    

class ActionSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=50)
    modifier = serializers.CharField(max_length=50)
    id = serializers.CharField(max_length=50)
