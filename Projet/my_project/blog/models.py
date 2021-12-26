from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import geocoder

SELLORRENT_CHOICES = (
    ('S', 'To Sell'),
    ('R', 'To Rent'),
)
CATEGORIES = (
    ('H', 'House'),
    ('A', 'Apartment'),
    ('G', 'Garage'),
)
#token for mapbox
token = 'pk.eyJ1Ijoic2FuZGllZ28xOCIsImEiOiJja3d4bGc2a3IwZHc3MnZsY2k1aGsycHE2In0.pHBEi0TiJZrYk0vIggf-7Q'

class Post(models.Model): #creation d'un Post
    title = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits= 15, decimal_places=2)
    sell_rent = models.CharField(default= 'S', max_length=10, choices=SELLORRENT_CHOICES)
    localisation = models.CharField(default='Bruxelles',max_length=100)
    address = models.TextField(default='Boulevard du Triomphe 1 , 1050 Bruxelles')
    lat = models.FloatField(blank=True, null=True)  # blank pour autoriser des valeurs vides
    long = models.FloatField(blank=True, null=True)
    category = models.CharField(default= 'H', max_length=10, choices=CATEGORIES)
    surface = models.DecimalField(default=0, max_digits= 8, decimal_places=2)
    content = models.TextField()
    image = models.ImageField(default='defaultAnnounce.jpg', upload_to='announce_pics')
    image2 = models.ImageField(default='defaultAnnounce.jpg', upload_to='announce_pics')
    image3 = models.ImageField(default='defaultAnnounce.jpg', upload_to='announce_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #ForeignKey = reférence à une autre classe (clé étrangère) --> on_delete=models.CASCADE --> signifie que lors de la suppression d'un User, tous ses posts seront supprimés aussi
    number_views = models.IntegerField(default=0)
    room_number = models.IntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):  # method that runs after our model is saved --> méthode qui existe déjà mais on va la réécrire afin d'ajouter des fonctionnalités
        super(Post, self).save(*args, **kwargs)

        #ouverture des 3 images
        img1 = Image.open(self.image.path)
        img2 = Image.open(self.image2.path)
        img3 = Image.open(self.image3.path)

        width1, height1 = img1.size #récupère les dimensions de img1
        width2, height2 = img2.size #récupère les dimensions de img2
        width3, height3 = img3.size #récupère les dimensions de img3

        # code pris : "https://pretagteam.com/question/django-image-compression-and-resize-not-working"

        #img1

        if width1 < height1: #si largeur < hauteur ca veut dire que ce n'est pas un carré alors on fait en sorte qu'il le devienne
            img1 = img1.crop((0, 0, width1, width1))

        elif height1 < width1: #si largeur > hauteur ca veut dire que ce n'est pas un carré alors on fait en sorte qu'il le devienne
            img1 = img1.crop(((width1 - height1) / 2, 0, (width1 + height1) / 2, height1))

        if width1 > 300 and height1 > 300:
            img1.thumbnail((300, 300)) #on rétrécit l'image pour faire en sorte que toutes les images soit 300x300 ou moins

        img1.save(self.image.path) #on sauvegarde les changement

        #img2

        if width2 < height2:
            img2 = img2.crop((0, 0, width2, width2))
        elif height2 < width2:
            img2 = img2.crop(( (width2 - height2) / 2, 0, (width2 + height2) / 2, height2 ))

        if width2 > 300 and height2 > 300:
            img2.thumbnail((300, 300))

        img2.save(self.image2.path)

        #img3

        if width3 < height3:
            img3 = img3.crop((0, 0, width3, width3))
        elif height3 < width3:
            img3 = img3.crop(( (width3 - height3) / 2, 0, (width3 + height3) / 2, height3 ))

        if width3 > 300 and height3 > 300:
            img3.thumbnail((300, 300))

        img3.save(self.image3.path)

        #code from https://geocoder.readthedocs.io/providers/Mapbox.html and https://www.youtube.com/watch?v=65flD9ScEQM
        g = geocoder.mapbox(self.address, key=token)
        g = g.latlng
        self.lat = g[0]
        self.long = g[1]
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk' : self.pk}) #redirige vers la page "post-detail" et enregistre la clé primaire du nouveau post


class Watchlist(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist_list')

    def save(self, *args, **kwargs):
        super(Watchlist, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.post}, {self.user}"









