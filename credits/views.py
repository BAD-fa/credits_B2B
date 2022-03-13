from django.db.models import Q
from django.db import transaction

from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication


from .serializers import OperationSerializer
from .models import Operation, User


class PostAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        operations = Operation.objects.filter(user=request.user.id)
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)

    def post(self, request):
        param = request.data.get('consumer')
        consumer = User.objects.get(username=param)
        supplier = User.objects.get(id=request.user.id)
        with transaction.atomic():
            operation1 = OperationSerializer(data={
                "user": supplier.id,
                "type": "S",
                "amount": -request.data.get('amount')
            })
            operation1.is_valid(raise_exception=True)
            operation1.save()
            operation2 = OperationSerializer(data={
                "user": consumer.id,
                "type": "R",
                "amount": request.data.get('amount')
            })
            operation2.is_valid(raise_exception=True)
            operation2.save()
        return Response(status=status.HTTP_201_CREATED)
