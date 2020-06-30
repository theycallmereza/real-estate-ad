import redis
import kavenegar

from django.conf import settings

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView, FormView
from django.views.decorators.csrf import csrf_protect

from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, PasswordResetForm, PhoneVerificationForm

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)
UserModel = get_user_model()


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class PasswordResetView(PasswordContextMixin, FormView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    token_generator = default_token_generator
    title = _('Password reset')

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'request': self.request,
            }
            form.save(**opts)
        except UserModel.DoesNotExist:
            form.add_error(None, 'این شماره موبایل پیدا نشد!')
            return self.form_invalid(form)
        return super().form_valid(form)


class PhoneVerificationView(LoginRequiredMixin, FormView):
    form_class = PhoneVerificationForm
    template_name = 'registration/phone_verification.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        r.set(request.user.phone_number, get_random_string(length=6, allowed_chars='1234567890'))
        r.expire(request.user.phone_number, 1800)
        print(r.get(request.user.phone_number).decode('utf-8'))
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = UserModel.objects.get(phone_number=request.user.phone_number)
        if form.is_valid():
            code = form.cleaned_data['verification_code']
            if r.exists(request.user.phone_number):
                redis_code = r.get(request.user.phone_number).decode('utf-8')
                if code == redis_code:
                    user.phone_number_verified = True
                    user.save()
                    return self.form_valid(form)
                else:
                    form.add_error(None, "کد تایید صحیح نمی باشد!")
                    return self.form_invalid(form)
