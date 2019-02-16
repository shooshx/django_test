from django.conf import settings
from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
class Team(models.Model):
    name = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=128, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "[Team:{}]".format(self.name)
        
class WarriorDef(models.Model):
    owner_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    owner_team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=80)
    wtype = models.IntegerField() # 1-one code, 2-two codes
    code1 = models.TextField()
    code2 = models.TextField()
    update_date = models.DateTimeField(default=timezone.now)
    updated_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='+') #'+' prevents reverse collision
    
    def __str__(self):
        return "[Warrior:"+self.title+"]"
        
 
      

        