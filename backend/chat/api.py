# Import Dependencies
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import Components
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from .models import Conversation, ConversationMessage

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user.id]))
    serializer = ConversationSerializer(conversations, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)

    return Response(serializer.data)


@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)

    for user in conversation.users.all():
        if user.id != request.user.id:
            sent_to = user


    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to
    )

    serializer = ConversationMessageSerializer(conversation_message)

    return Response(serializer.data)



