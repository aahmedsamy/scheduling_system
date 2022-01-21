from django.contrib import admin

# Register your models here.
from .models import Slot, Meeting

admin.site.register(Slot)
admin.site.register(Meeting)
