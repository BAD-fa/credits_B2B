from rest_framework import serializers

from .models import Operation


class OperationSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()

    class Meta:
        model = Operation
        fields = ['user', 'amount', 'type', 'date', 'status', 'message']
