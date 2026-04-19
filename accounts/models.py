from django.db import models

from django.contrib.auth.models import User
#why signales:
# 1. To automatically create a profile when a new user is created.
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    
    #knlinkiw bin l user o lprofile bsh ila creayina shi profil jdid ki tkrya user
    # ykoun l user id l profile id
    # This field is required to create a one-to-one relationship with the User model.
    # how it woks:
    # 1. When a new user is created, a corresponding profile is created automatically.
    # 2. When a profile is accessed, the related user can be accessed through the `user` field.
    # 3. When a user is deleted, the corresponding profile is also deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return str(self.user)
    
@receiver(post_save, sender=User)  
def create_user_profile(sender, instance, created , **kwargs):
    #sender: the model class that sent the signal (User in this case)
    #instance: the actual instance of the model that was created (the new User instance)
    #created: a boolean indicating whether a new instance was created (True) or updated (False)
    #**kwargs: additional keyword arguments (not used here)
    if created:
        Profile.objects.create(
            user = instance
        )