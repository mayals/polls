from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser,Voter,AdminProfile,OwnerProfile,VoterProfile
from django.conf import settings
        
        
#################################### AdminProfile signal ###########################################################3        
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_Admin_profile(sender,instance,created,**kwargs):
    if created:
        user=instance
        AdminProfile.objects.create(user=instance)
        

       
 
#################################### OwnerProfile signal ###########################################################3
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_owner_profile(sender,instance,created,**kwargs):
    if created:
        if instance.role == 'OWNER' : 
            #print("instance.role ="+str(instance.role))
            OwnerProfile.objects.create(user=instance)  
            
        
        
#################################### VoterProfile signal ###########################################################
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_voter_profile(sender,instance,created,**kwargs):
    if created:
        if instance.role == 'VOTER' : 
            #print("instance.role ="+str(instance.role))
            VoterProfile.objects.create(user=instance)