from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        rating_post_author = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum']*3
        rating_comments_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_comments_post_authors = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        self.rating = rating_post_author+rating_comments_author+rating_comments_post_authors
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique = True)
    subscribers = models.ManyToManyField(User)

    
    def __str__(self):
        return self.name.title()

article = 'AR'
news = 'NW'
NewsArticles = [
    (article,'Статья'),
    (news,'Новость')
]


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,choices = NewsArticles)
    time_in = models.DateTimeField (auto_now_add = True)
    categories = models.ManyToManyField(Category, through=PostCategory)
    title = models.CharField(max_length = 100)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title.title()}:{self.text[:150]}'
    
    

    def like(self):
        self.rating +=1
        self.save()
    
    def dislike(self):
        self.rating -=1
        self.save()
    
    def preview(self):
        return self.text if len(self.text) < 124 else self.text[:124] + '...'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateTime = models.DateTimeField (auto_now_add = True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()
    
    def dislike(self):
        self.rating -=1
        self.save()







