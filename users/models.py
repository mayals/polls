from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone



class Gender(models.TextChoices):
        MALE   = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
class CommonProfile(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=False)
    last_name  = models.CharField(max_length=50 , null=True, blank=False)
    email      = models.EmailField(unique=True, null=True, blank=False)
    age        = models.IntegerField(null=True, blank=False)
    country    = models.CharField(max_length=200, blank=False, null=True)
    gender     = models.CharField(max_length=50, choices=Gender.choices, default=Gender.MALE)  
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False,null=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True,null=True)
    
    
    # note : Abstract Models cannot be instantiated
    class Meta :
        abstract = True
        

     
     
        
#################################### CustomUser - Admin ###########################################################3
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        VOTER = "VOTER", "Voter"
        
    # user type at start
    base_role = "ADMIN"
          
    # to decide What type of user are you?      
    role   = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.role = self.base_role
            print(self.role)
            return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("users:user-detail", kwargs={"username": self.username})


    def __str__(self):
            return str(self.username)
        
        
        
        
#################################### AdminProfile ###########################################################3
# Note: AdminProfile is created by a signal
class AdminProfile(CommonProfile):   
    user   = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    polls_count = models.IntegerField(null=True, blank=True)
    votes_count = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.user.username)


#################################### Owner ###########################################################3
class OwnerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=CustomUser.Role.OWNER)
       
class Owner(CustomUser):
    base_role = CustomUser.Role.OWNER
    objects = OwnerManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)
    
    
    
#################################### OwnerProfile ###########################################################3

class OwnerProfile(CommonProfile):   
    user   = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    polls_count = models.IntegerField(null=True, blank=True)
    votes_count = models.IntegerField(null=True, blank=True)

    
    def __str__(self):
        return str(self.user.username)




#################################### Voter ###########################################################3
class VoterManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=CustomUser.Role.VOTER)
  
class Voter(CustomUser):
    base_role = CustomUser.Role.VOTER
    objects = VoterManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = CustomUser.Role.VOTER
            return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)



#################################### VoterProfile ###########################################################3
class VoterProfile(CommonProfile):
    user        = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    votes_count = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.user.username)