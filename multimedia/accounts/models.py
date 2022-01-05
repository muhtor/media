from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_superuser=False):
        if is_superuser:
            user = self.model(email=email)
        else:
            user = self.model(email=email)
        if not email:
            raise ValueError('Users must have a email')
        if password is not None:
            user.set_password(password)
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_staffuser(self, email, password):
        if not password:
            raise ValueError('staff/admins must have a password.')
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, password):
        if not password:
            raise ValueError('superusers must have a password.')
        user = self.create_user(email=email, password=password, is_superuser=True)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name='email address', unique=True, max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def has_perm(self, perm, obj=None):
        return True  # does user have a specific permision, simple answer - yes

    def has_module_perms(self, app_label):
        return True  # does user have permission to view the app 'app_label'?


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Music(models.Model):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "Musics"


class Movie(models.Model):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "Movies"
