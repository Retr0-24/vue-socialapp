# Import Dependencies
from django.db import models
import uuid

# Import Components
from account.models import User
from post.models import Post

class Notification(models.Model):
    NEWFRIENDREQUEST = 'new_friendrequest'
    ACCEPTEDFRIENDREQUEST = 'accepted_friendrequest'
    REJECTEDFRIENDREQUEST = 'rejected_friendrequest'
    POST_LIKE = 'post_like'
    POST_COMMENT = 'post_comment'

    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEWFRIENDREQUEST, 'New Friend Request'),
        (ACCEPTEDFRIENDREQUEST, 'Accepted Friend Request'),
        (REJECTEDFRIENDREQUEST, 'Rejected Friend Request'),
        (POST_LIKE, 'Post Like'),
        (POST_COMMENT, 'Post Comment'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


