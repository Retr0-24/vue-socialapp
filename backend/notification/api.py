# Import Dependencies
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Import Componenents
from .serializers import NotificationSerializer
from .models import Notification


@api_view(['GET'])
def notifications(request):
    received_notifications = request.user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(received_notifications, many=True)

    return JsonResponse(serializer.data, safe=False)