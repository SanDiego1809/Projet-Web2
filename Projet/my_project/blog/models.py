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
    #construction_year
    #pieces = models.DecimalField(default=0, max_digits= 3)
    content = models.TextField()
    image = models.ImageField(default='defaultAnnounce.jpg', upload_to='announce_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #reférence à une autre classe (clé étrangère)
    #on_delete=models.CASCADE --> signifie que lors de la suppression d'un User, tous ses posts seront supprimés aussi

    def save(self, *args, **kwargs):  # method that runs after our model is saved --> méthode qui existe déjà mais on va la réécrire afin d'ajouter des fonctionnalités
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        width, height = img.size

        # check if the current img is more thant 300 px (chosen by Corey Shafer)
        # code pris : "https://pretagteam.com/question/django-image-compression-and-resize-not-working"
        if height < width:

            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:

            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.image.path)

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











