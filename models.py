import os
import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from social_django.models import UserSocialAuth

# In order to import these, you have to
# use tha utilities code from my other repo
from ..utilities.unique.functions import get_random_string
from ..utilities.time_calculator.functions import days_hence


def get_upload_path(instance, filename):
    return os.path.join(
        settings.USERS_LOGO_DIR, get_random_string(4, 'user_', '.jpg'))


class SimpleUser(models.Model):
    """
    Definition of SimpleUser Model. This model extends the default
    Django User model with one to one field
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='simple_user')

    middle_name = models.CharField(max_length=255, blank=True, null=True)

    birth_date = models.DateField(blank=False, null=True,
                                  help_text="User's birth date")

    mobile_number = models.CharField(max_length=40, blank=True, null=True,
                                     help_text=_(u'Mobile Number'))

    home_number = models.CharField(max_length=40, blank=True, null=True,
                                   help_text=_(u'Home Number'))

    contact_time_min = models.TimeField(blank=True, null=True,
                                        help_text=_(u"Contact user min time"))

    contact_time_max = models.TimeField(blank=True, null=True,
                                        help_text=_(u"Contact user max time"))

    address = models.CharField(max_length=60, blank=True, null=True,
                               help_text=_(u'Address'))

    city = models.CharField(max_length=60, blank=True, null=True,
                            help_text=_(u'City'))

    website = models.URLField(blank=True, null=True,
                              help_text=_(u'Personal website'))

    avatar = models.ImageField(
        default='', blank=True, upload_to=get_upload_path)

    created_on = models.DateTimeField(auto_now_add=True)

    last_updated = models.DateTimeField(auto_now=True)

    date_activated = models.DateTimeField(null=True, blank=True)

    hide_contact_details = models.NullBooleanField(default=True,
                                                   help_text=_(u'contact data will be hidden'),  # noqa
                                                   )

    activation_key = models.CharField(max_length=40, blank=True)

    key_expires = models.DateTimeField(default=days_hence)

    facebook_link = models.CharField(max_length=200, blank=True,
                                     help_text=_(u'Facebook profile link'))

    subscribed = models.BooleanField(default=True, help_text=_(u'Send emails'))

    @property
    def email(self):
        return self.user.email

    # If user is registered with social facebook
    def get_avatar_url(self, geometry=settings.AVATAR_DIMENSIONS, **kwargs):
        user = self.user
        try:
            social_user = user.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            social_user = None

        if social_user:
            try:
                response = requests.get('https://graph.facebook.com/' + str(
                    social_user.uid) + '/picture?width=251&height=251&redirect=0')  # noqa

                j = response.json()
                j['data']['url']
                return j['data']['url']
            except (AttributeError, IOError, KeyError, IndexError):
                return False

    @receiver(pre_delete)
    def delete_user(sender, instance, **kwargs):
        if isinstance(instance, SimpleUser):
            instance.avatar.delete()

    def __unicode__(self):
        return self.user.get_full_name()
