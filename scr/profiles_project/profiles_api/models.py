from django.db import models

from django.urls import reverse

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

# Create your models here.

class UserProfileManager(BaseUserManager):
    """Helps Django work with out custom user model"""

    def create_user(self, email, name, password=None):
        """Creates a new user profile object"""

        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email = email, name = name)

        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser with given details"""

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a "user profile" inside our system."""

    email = models.EmailField(max_length = 255, unique=True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a users full name"""

        return self.name

    def get_short_name(self):
        """Used to get the users short name"""

        return self.name

    def __str__(self):
        """Django uses this when it needs to convert the object into a string"""

        return self.email


class ProfileFeedItem(models.Model):
    """Profiles status update"""

    user_profile = models.ForeignKey('UserProfile' ,on_delete = models.CASCADE)
    status_text = models.CharField(max_length = 255)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        """Return the model as a string."""

        return self.status_text

class PostItem(models.Model):
    """Posts service hours opportunities"""

    title = models.CharField(max_length = 100)
    slug = models.SlugField(max_length=160,blank=True,editable=False)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    user_profile = models.ForeignKey('UserProfile', on_delete = models.CASCADE)

    def __unicode__(self):
        """Simplifies display of description of the object"""
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (),
                {
                    'slug' :self.slug,
                })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(PostItem, self).save(*args, **kwargs)

class Candidate(models.Model):
    user = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255, unique=True)

    def __unicode__(self):
        """returns as a string"""

        return unicode(self.user)

    def get_absolute_url(self):
        """gets the url"""
        return reverse('user_detail' , kwargs = {'pk' : str(self.id) })
