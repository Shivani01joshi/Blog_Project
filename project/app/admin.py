from django.contrib import admin
from django.contrib import admin

from .models import Blog,Comment

#admin.site.register(Blog)
admin.site.register(Blog)
# Register your models here.
admin.site.register(Comment)