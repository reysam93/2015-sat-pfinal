from django.db import models
from datetime import date, time, datetime, MINYEAR
from django.contrib.auth.models import User


class Comment(models.Model):
    nick = models.CharField(max_length=30, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default='')


class Activity(models.Model):
    title = models.CharField(default = "", max_length=150)
    type = models.CharField(default = "", max_length=300)
    price = models.PositiveIntegerField(default = 0)
    date = models.DateField(default = date(MINYEAR, 1, 1))
    time = models.TimeField(default = time(0,0,0))
    long = models.BooleanField(default = False)
    url = models.CharField(default = "", max_length=300)
    likes = models.PositiveIntegerField(default = 0)
    whoLikes = models.ManyToManyField(User)
    comments = models.ManyToManyField(Comment)
    class Meta:
        ordering = ['date', 'time']


class UserCSS(models.Model):
    bgCont = models.CharField(max_length=30, default = 'white')
    bgBanner = models.CharField(max_length=30, default = 'white')
    bgCopyRigth = models.CharField(max_length=30, default = 'white')
    bgLogBox = models.CharField(max_length=30, default = '#999999')
    bgMenu = models.CharField(max_length=30, default = 'black')
    wordColorCont = models.CharField(max_length=30, default = 'black')
    wordColorBanner = models.CharField(max_length=30, default = '#778899')
    wordColorCopyRigth = models.CharField(max_length=30, default = 'black')
    wordColorLogBox = models.CharField(max_length=30, default = 'black')
    wordColorMenu = models.CharField(max_length=30, default = '#999999')
    wordSizeCont = models.PositiveIntegerField(default = 12)
    wordSizeBanner = models.PositiveIntegerField(default = 25)
    wordSizeCopyRigth = models.PositiveIntegerField(default = 12)
    wordSizeLogBox = models.PositiveIntegerField(default = 12)
    wordSizeMenu = models.PositiveIntegerField(default = 15)


class Selected(models.Model):
    act = models.ForeignKey(Activity, primary_key=True)
    date = models.DateField(default = date(MINYEAR, 1, 1))


class UserPage(models.Model):
    nick = models.CharField(max_length=30, default='')
    title = models.CharField(max_length=50, default='')
    nActs = models.PositiveIntegerField(default = 0)
    description = models.TextField(default = '')
    selected = models.ManyToManyField(Selected)
    updated = models.DateTimeField(auto_now=True)
    css = models.ForeignKey(UserCSS)
