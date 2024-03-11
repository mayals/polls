from django.contrib import admin
from .models import CustomUser,Owner,Voter,OwnerProfile,VoterProfile
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Owner)
admin.site.register(OwnerProfile)
admin.site.register(Voter)
admin.site.register(VoterProfile)