from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login
from .forms import UserSignUpForm, UserProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from .models import *
from django.core.mail import EmailMessage
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        addresses = [{'id': address.pk,
                      'address': address.address,
                      'postal_code': address.postal_code,
                      'city': address.city,
                      'country': address.country} for address in Addresses.objects.filter(user=user)]
        numbers = [{'id': number.pk,
                    'country_code': number.country_code,
                    'number': number.number} for number in Numbers.objects.filter(user=user)]
        return Response({
            'token': token.key,
            'last_login': user.last_login,
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'admin': user.is_superuser,
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'addresses': addresses,
            'numbers': numbers,
        })


def userSignup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        form = UserSignUpForm()
    return render(request, 'commons/signup.html', {'form': form})


def activateAccount(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


class UserProfile(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'
