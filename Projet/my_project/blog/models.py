from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model): #creation d'un Post
    title= models.CharField(max_length=100)
    content= models.TextField()
    date_posted= models.DateTimeField(default=timezone.now)
    author= models.ForeignKey(User, on_delete=models.CASCADE) #reférence à une autre classe (clé étrangère)
    #on_delete=models.CASCADE --> signifie que lors de la suppression d'un User, tous ses posts seront supprimés aussi

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk' : self.pk}) #redirige vers la page "post-detail" et enregistre la clé primaire du nouveau post

