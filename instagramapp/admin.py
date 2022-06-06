from django.contrib import admin
from .models import Image,Profile,Comments
# Register your models here.


admin.site.register(Image)
admin.site.register(Comments)
admin.site.register(Profile)