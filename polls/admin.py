from django.contrib import admin
from .models import Poll,Choice,Category


admin.site.register(Category)
admin.site.register(Poll)
admin.site.register(Choice)

