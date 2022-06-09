from django.contrib import admin
from .models import Post,Profile,Comments
# Register your models here.


admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Profile)