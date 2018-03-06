import os
import requests
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from social_django.models import UserSocialAuth

# In order to import these, you have to
# use tha utilities code from my other repo
# Check READEME.md file
from ..utilities.unique.functions import get_random_string
from ..utilities.time_calculator.functions import days_hence


def get_upload_path(instance, filename):
    return os.path.join('uploads/users', get_random_string(4, 'user_', '.jpg'))


class SimpleUser(models.Model):
    """
    Definition of SimpleUser Model. This model extends the default
    Django User model with one to one field. Validation will occur at the forms
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

    # After March 25, 2018, be ware of the default value (EU GDPR 2018)
    hide_contact_details = models.NullBooleanField(default=None,
                                                   help_text=_(u'Contact data will be hidden'),  # noqa
                                                   )
    # (EU GDPR 2018)
    subscribed = models.BooleanField(default=True, help_text=_(u'Send emails'))

    activation_key = models.CharField(max_length=40, blank=True)

    # Key expires after one day, (default days_hence)
    # If you set here a day number, default=days_hence(5)
    # On any makemigration a new migration file will be created
    key_expires = models.DateTimeField(default=days_hence)

    facebook_link = models.CharField(max_length=200, blank=True,
                                     help_text=_(u'Facebook profile link'))

    @property
    def email(self):
        return self.user.email

    # If user is registered with facebook
    def get_avatar_url(self, geometry='251x251', **kwargs):
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

    @property
    def key_expired(self):
        today = timezone.now()
        if self.key_expires > today:
            return False
        return True

    @receiver(pre_delete)
    def delete_user(sender, instance, **kwargs):
        if isinstance(instance, SimpleUser):
            instance.avatar.delete()

    def __unicode__(self):
        return self.user.get_full_name()
