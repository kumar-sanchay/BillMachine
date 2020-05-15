from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from PIL import Image
from django.urls import reverse
from company.models import Company


class UserModel(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', unique=True)
    username = models.SlugField(max_length=25, unique=True)
    first_name = models.CharField(max_length=25, blank=False, null=False)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    city = models.CharField(max_length=30, blank=False, null=False)
    state = models.CharField(max_length=30, blank=False, null=False)
    avatar = models.ImageField(verbose_name='avatar', upload_to='profile/pic/', blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'city', 'state']

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return '{}'.format(self.username)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.username:
            username = self.email.split('@')
            self.username = username[0]
            super(UserModel, self).save(*args, **kwargs)
        if self.avatar:
            image = Image.open(self.avatar)
            size = (200, 200)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.avatar.path)

    def get_absolute_url(self):
        return reverse('authentication:profile_url')


class RecentActivities(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='activity_user')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='activity_company',
                                null=True, blank=True)
    bill = models.ForeignKey('fileStorage.FileStorage', on_delete=models.SET_NULL, related_name='activity_bill',
                             null=True, blank=True)
    activity = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Recent Activity'
        verbose_name_plural = 'Recent Activities'

