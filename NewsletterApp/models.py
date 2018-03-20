from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import requests
import json

# just for default values in model Letter
url = "https://api.sendgrid.com/v3/stats?limit=1&offset=1&aggregated_by=month&start_date=2018-03-01&end_date=2018-04-01"
payload = "{}"
headers = {'authorization': 'Bearer <<API_KEY>>'}
response = requests.request("GET", url, data=payload, headers=headers)
result_api = json.loads(response.text)
a = result_api[0]['stats'][0]['metrics']
clicks = a['unique_clicks']
opened_email = a['unique_opens']
delivered_email = a['delivered']


# Create your models here.
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.user)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Letters(models.Model):

    sent_letters = models.PositiveIntegerField(default=delivered_email)
    read_letters = models.PositiveIntegerField(default=opened_email)
    return_user = models.PositiveIntegerField(default=clicks)

    def __str__(self):
        return 'Letter'
