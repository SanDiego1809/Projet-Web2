from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #CASCADE : si je supprime l'utilisateur, le profil sera supprimé aussi. Mais si je supprime le profil, l'utilisateur ne sera pas supprimé
    image = models.ImageField(default='default.jpg', upload_to='profile_pics') #default = image par défaut si l'user ne choisit aucune pdp

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

