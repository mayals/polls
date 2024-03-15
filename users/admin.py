from django.contrib import admin
from .models import CustomUser,Owner,Voter,AdminProfile,OwnerProfile,VoterProfile
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AdminProfile)

admin.site.register(Owner)
admin.site.register(OwnerProfile)

admin.site.register(Voter)
admin.site.register(VoterProfile)