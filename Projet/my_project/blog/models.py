from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

SELLORRENT_CHOICES = (
    ('S', 'To Sell'),
    ('R', 'To Rent'),
)

class Post(models.Model): #creation d'un Post
    title = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits= 15, decimal_places=2)
    sell_rent = models.CharField(default= 'S', max_length=10, choices=SELLORRENT_CHOICES)
    content= models.TextField()
    image = models.ImageField(default='defaultAnnounce.jpg', upload_to='announce_pics')
    date_posted= models.DateTimeField(default=timezone.now)
    author= models.ForeignKey(User, on_delete=models.CASCADE) #reférence à une autre classe (clé étrangère)
    #on_delete=models.CASCADE --> signifie que lors de la suppression d'un User, tous ses posts seront supprimés aussi

    def save(self, *args, **kwargs):  # method that runs after our model is saved --> méthode qui existe déjà mais on va la réécrire afin d'ajouter des fonctionnalités
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        # check if the current img is more thant 300 px (chosen by Corey Shafer)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)  # save the changes

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk' : self.pk}) #redirige vers la page "post-detail" et enregistre la clé primaire du nouveau post



