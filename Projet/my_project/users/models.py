from django.db import models
from django.contrib.auth.models import User
from PIL import Image

SELLORRENT_CHOICES = (
    ('S', 'To Sell'),
    ('R', 'To Rent'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #CASCADE : si je supprime l'utilisateur, le profil sera supprimé aussi. Mais si je supprime le profil, l'utilisateur ne sera pas supprimé
    image = models.ImageField(default='default.jpg', upload_to='profile_pics') #default = image par défaut si l'user ne choisit aucune pdp
    price_preference = models.DecimalField(default=0, max_digits=15, decimal_places=2) #prix maximum préféré
    localisation_preference = models.CharField(default='Bruxelles', max_length=100) #localisation préférée
    sell_rent_preference = models.CharField(default='S', max_length=10, choices=SELLORRENT_CHOICES) #a vendre ou a louer

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs): #method that runs after our model is saved --> méthode qui existe déjà mais on va la réécrire afin d'ajouter des fonctionnalités
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        #check if the current img is more thant 300 px (chosen by Corey Shafer)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) #resize the image to 300x300
            img.save(self.image.path) #save the changes

