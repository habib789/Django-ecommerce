from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    publish_date = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(upload_to='post/images', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-publish_date']


class PostComment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk})