from django.db import models

#video_dir = r"D:\M Tech DSE Bits\Semester 3\Information Retrieval\Assignments\Assignment 2\video_search\Data\\"

# Create your models here.
class video(models.Model):
    name = models.CharField(max_length = 1000)
    author = models.CharField(max_length = 1000)
    videoFile = models.FileField(upload_to='video')
    pubDate = models.DateTimeField(auto_now_add = True, blank = True)
    thumbnail = models.ImageField(upload_to="image")
    
    def __str__(self):
        return self.name
    