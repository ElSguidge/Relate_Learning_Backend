from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    residence = models.CharField(max_length=100, blank=True, null=True)
    organisation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    time_zone = models.CharField(max_length=100, blank=True, null=True)
    active_id = models.BooleanField(default=True)
    avatar = models.ImageField(null=True, blank=True, upload_to ='uploads/profile_pics/',default='uploads/default.jpg')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        rgb_img= img.convert('RGB')
        
        fixed_image = ImageOps.exif_transpose(rgb_img)
        if fixed_image.height > 1125 or fixed_image.width > 1125:
           fixed_image.thumbnail((400,400))
        fixed_image.save(self.avatar.path,quality=70,optimize=True)

class ProfileStatus(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status_content = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'statuses'

    def __str__(self):
        return str(self.user_profile)



    