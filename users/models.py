from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self) -> str:
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        upper = (height - size) // 2
        right = (width + size) // 2
        lower = (height + size) // 2

        img = img.crop((left, upper, right, lower))
        
        if height > 300 or width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)