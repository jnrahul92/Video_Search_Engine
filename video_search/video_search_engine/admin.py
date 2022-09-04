from django.contrib import admin
from .models import video
# Register your models here.

class videoAdmin(admin.ModelAdmin):
    list_display = ("name","author","videoFile","pubDate","thumbnail")
    
admin.site.register(video, videoAdmin)