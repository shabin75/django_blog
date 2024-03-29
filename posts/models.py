from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='author_user',verbose_name='User')
    profile_pic = models.ImageField(upload_to='pics')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=111)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='pics')
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=True)
    content = HTMLField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('post-update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post-delete', kwargs={'id': self.id})
    @property
    def get_comments(self):
        return self.comments.all()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='comments', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username
