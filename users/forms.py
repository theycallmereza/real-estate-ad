from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

import kavenegar

UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'پسورد ها باهم مطابقت ندارند',
    }

    class Meta:
        model = get_user_model()
        fields = ['phone_number']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['phone_number']


class PasswordResetForm(forms.Form):
    phone_number = forms.CharField(label='شماره موبایل', max_length=11,
                                   validators=[RegexValidator(regex=r'09(\d{9})$')])

    def send_sms(self, phone_number, reset_link):
        try:
            api = kavenegar.KavenegarAPI(settings.KAVENEGAR_APIKEY)
            message = f'برای بازیابی رمز عبور روی لینک زیر کلیک کنید \n {reset_link}'
            params = {
                'sender': '1000596446',
                'receptor': phone_number,
                'message': message,
            }
            response = api.sms_send(params)
            print(response)
        except kavenegar.APIException as e:
            print(e)
        except kavenegar.HTTPException as e:
            print(e)

    def get_users(self, phone_number):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        return UserModel.objects.get(phone_number=phone_number)

    def save(self, domain_override=None,
             use_https=False, token_generator=default_token_generator,
             request=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        phone_number = self.cleaned_data["phone_number"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        user = self.get_users(phone_number)
        user_phone_number = user.phone_number
        # context = {
        #     'phone_number': user_phone_number,
        #     'domain': domain,
        #     'site_name': site_name,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'user': user,
        #     'token': token_generator.make_token(user),
        #     'protocol': 'https' if use_https else 'http',
        #     # **(extra_email_context or {}),
        # }
        protocol = 'https' if use_https else 'http'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        reset_link = protocol + '://' + domain + reverse('password_reset_confirm',
                                                         args=[uid, token])
        print(reset_link)
        self.send_sms(user_phone_number, reset_link)


class PhoneVerificationForm(forms.Form):
    verification_code = forms.CharField(label='کد تایید', max_length=6)
