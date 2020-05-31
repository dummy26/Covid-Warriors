from django.db import models
from PIL import Image

# Remove when homepage and article tab are ready 
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='pics')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        
        if img.height>300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.title
