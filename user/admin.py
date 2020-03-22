from django.contrib import admin

# Register your models here.
from .models import Profile

admin.site.register(Profile)

# admin.site.site_header = "MEDICUST"
# admin.site.site_title = "Medicust Admin Portal"
# admin.site.index_title = "Welcome to MEDICUST Portal"
