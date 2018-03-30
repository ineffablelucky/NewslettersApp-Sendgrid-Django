from django.shortcuts import render, HttpResponse
from NewsletterApp.forms import RegisterationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.conf import settings
from .models import Letters
import sendgrid
import os
import requests
import json

# to see api data
def api_request(request):

    # data api is created
    url = "https://api.sendgrid.com/v3/stats?limit=1&offset=1&aggregated_by=month&start_date=2018-03-01&end_date=2018-04-01"

    payload = "{}"
    headers = {'authorization': 'Bearer <<API_KEY>>'}

    response = requests.request("GET", url, data=payload, headers=headers)
    result_api = json.loads(response.text)
    a = result_api[0]['stats'][0]['metrics']

    # update_or_create() https://docs.djangoproject.com/en/2.0/ref/models/querysets/#update-or-create
    obj, created = Letters.objects.update_or_create(
    id=0,
    defaults={'sent_letters': a['delivered'], 'read_letters': a['unique_opens'], 'return_user': a['unique_clicks']},
)
    #model_data = Letters(sent_letters=a['delivered'], read_letters=a['unique_opens'], return_user=a['unique_clicks'])
    #model_data.
    return HttpResponse(result_api)


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        try:
            if form.is_valid:
                form.save()
                return HttpResponse("""<p>Registration Done!!</p>""")

        except ValueError:  # have to test it out
            return HttpResponse("\
            <h1>Go Back, Read The Instructions and Then Enter Data Carefully.\
            </h1>")
    else:

        form = RegisterationForm()
        context = {'form': form}
        return render(request, 'NewsletterApp/register_form.html', context)


# sending email
def send_email(request):

    all_users = User.objects.all()
    subject ='Newsletter'
    from_email = settings.DEFAULT_FROM_EMAIL

    # newsletter content below. can also entered via txt file or html file
    content_message = 'Newsletter content <a href="https://programmedtocode.wordpress.com/>CLICK LINK</a>"'
    for user_email in all_users:
        """
        to_email = [user_email.email]
        context = {
        'email' : from_email,
        'message' : content_message,
        }

        final_send_content = get_template('Newsletter_content.txt').render(context)
        """

        if user_email.username == 'owner':  # to ignore superuser 'owner' 
            continue
        else:
            to_email = user_email.email
            send_mail(subject,content_message,from_email, [to_email], fail_silently=True)

    return HttpResponse("mail sent")
