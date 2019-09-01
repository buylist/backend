from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.contrib import auth
from mainapp.models import Buyer
from rest_framework.authtoken.models import Token
from buylist.settings import SOCIALIZER
import requests
import pybase64
import hashlib
import json
import os


def test_login(request):
    buyer = Buyer.objects.filter(email='buylist.project+1@gmail.com').first()
    auth.login(request, buyer)
    request.session.set_expiry(0)
    return HttpResponseRedirect(reverse('mainapp:main_web_page'))


def login(request):
    if request.method == 'POST':
        buyer = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if buyer and buyer.is_active:
            auth.login(request, buyer)
            request.session.set_expiry(0)
    return HttpResponseRedirect(reverse('mainapp:main_web_page'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('mainapp:entrance_page'))


# запрос в гугл за authorization code, подробнее https://developers.google.com/identity/protocols/OpenIDConnect
def google_login(request):
    google = SOCIALIZER['google']
    url_conf = '?'
    url_params = {
        'client_id': google['OAUTH2_KEY'],
        'redirect_uri': google['redirect_uri'],
        'response_type': google['response_type'],
        'scope': google['scope'],
        'state': hashlib.sha256(os.urandom(1024)).hexdigest(),
    }

    if 'web' in request.GET and request.GET['web'] == 'yes':
            url_params.update({'redirect_uri': google['redirect_uri_web']})

    lenght = len(url_params)

    for i, (key, val) in enumerate(url_params.items()):
        url_conf += key + '=' + val
        if i < lenght - 1:
            url_conf += '&'

    response = HttpResponseRedirect(google['request_url']+url_conf, request.POST)
    response.set_cookie(key='state', value=url_params['state'])

    request.session['state'] = url_params['state']

    return response


# обработка ответа гугла после запроса google_login
def google_response(request):
    def decode_jwt(t):
        _, payload, _ = t.split('.')
        payload = pybase64.urlsafe_b64decode(payload + '==')
        return json.loads(payload)

    def get_buyer():
        auth_response = requests.post('https://oauth2.googleapis.com/token', data=auth_request).json()

        response_data = decode_jwt(auth_response['id_token'])

        print(f"response_data {response_data}")

        if Buyer.objects.filter(email=response_data['email'], social_id=response_data['sub']).first():
            buyer = Buyer.objects.filter(email=response_data['email'], social_id=response_data['sub']).first()
        else:
            if not Buyer.objects.filter(email=response_data['email']).first():
                user_name = response_data.get('name', response_data['email'])
                buyer = Buyer.objects.create_user(username=user_name, email=response_data['email'], password=os.urandom(10))
                setattr(buyer, 'social_id', response_data['sub'])
            else:
                buyer = Buyer.objects.filter(email=response_data['email']).first()
                setattr(buyer, 'password', os.urandom(10))
                setattr(buyer, 'social_id', response_data['sub'])
                buyer.save()

        return buyer

    google = SOCIALIZER['google']
    auth_request = {
        'code': request.GET['code'],
        'client_id': google['OAUTH2_KEY'],
        'client_secret': google['OAUTH2_SECRET'],
        'grant_type': google['grant_type'],
        'redirect_uri': google['redirect_uri'],
    }

    session = Session.objects.get(session_key=request.COOKIES['sessionid'])
    state = session.get_decoded().get('state')

    if request.resolver_match.url_name == 'web_profile':
        auth_request.update({'redirect_uri': google['redirect_uri_web']})

        if request.GET['state'] == state:
            buyer = get_buyer()
            auth.login(request, buyer)
            request.session.set_expiry(0)

            return HttpResponseRedirect(reverse('mainapp:main_web_page'))
        return HttpResponse('sorry, but STATE is not valid', status=401)
    else:
        if 'state' in request.GET and request.GET['state'] == state:

            buyer = get_buyer()

            token_obj, _ = Token.objects.get_or_create(user=buyer)
            buy_list_token = token_obj.key

            context = {
                'token': {'token': buy_list_token},
            }

            return HttpResponse(JsonResponse(context['token']))
        return render(request, 'socializer/socializer.html', {'token': 'GOOGLE RESPONSE ERROR: NOT VALIDATED STATE'})
