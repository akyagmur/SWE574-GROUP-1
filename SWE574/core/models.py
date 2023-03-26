# Import from external packages
from uuid import uuid4

# Import from django modules
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel
# Import user model from django
from django.contrib.auth.models import User

# Create your models here.

# User = get_user_model()

# override the default user model
class User(User):
    class Meta:
        proxy = True


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_user = models.IntegerField(unique=True)
    bio = models.TextField(default="Write something here")
    profile_image = models.ImageField(upload_to="profile_images", default="profile_images/blank-profile-picture.png")
    background_image = models.ImageField(upload_to="background_images",
                                         default="background_images/bg-image-5.jpg")
    followers = ArrayField(models.IntegerField(), default=list, blank=True)
    following = ArrayField(models.IntegerField(), default=list, blank=True)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


class Post(TimeStampedModel):
    # Fields that are automatically filled
    post_id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    owner_username = models.TextField(max_length=100)
    #likes with created
    likes = models.ManyToManyField(User, related_name='liked_posts', through='Like')
    #bookmarks with created
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_posts', through='Bookmark')
    # posts must belong to a user
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', default=None)
    # Fields that are filled by owner user
    link = models.URLField(blank=False)  # URLField cannot be empty, this not twitter :)
    caption = models.TextField(blank=True)  # Caption can be empty
    # Fields that are filled by other users
    bookmarked_by = ArrayField(models.IntegerField(), default=list, blank=True, )
    num_of_bookmarks = models.IntegerField(default=0)
    # Preview attributes
    title = models.TextField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    preview_image = models.TextField(max_length=200, blank=True)
    # Many-to-many field for tags
    tags = models.ManyToManyField('Tag', related_name='posts', default=None)
    spaces = models.ManyToManyField('Space', related_name='posts', default=None)

    def __str__(self):
        return self.owner_username
    
    def total_likes(self):
        return self.likes.count()
    def tags_as_json_string(self):
        """ name: tag_name, id: tag_id """
        return [{"name": tag.name, "id": tag.id} for tag in self.tags.all()]
class Like(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_by_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_liked')

    def __str__(self):
        return self.user.username
    
class Bookmark(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarked_by_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_bookmarked')

    def __str__(self):
        return self.user.username

class Tag(TimeStampedModel):
    name = models.CharField(max_length=25, unique=True)


class Space(TimeStampedModel):
    name = models.CharField(max_length=25, unique=True)
