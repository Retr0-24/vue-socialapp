# Import Dependencies
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import Components
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from .models import Conversation, ConversationMessage
from account.models import User


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


@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

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



