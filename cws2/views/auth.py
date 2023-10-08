from captcha.fields import ReCaptchaField
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.forms.utils import ErrorList
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from cws2.models.user import User
from cws2.views.base import FormView


class CreateAccountForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "captcha"]


class CreateAccountView(FormView):
    body_colour = "orange"

    form_class = CreateAccountForm
    success_url = reverse_lazy("login")

    verb = _("Create account")
    verb_icon = "fa-user-plus"
    breadcrumb_root = False

    field_classes = {"captcha": "form__field--no-label"}

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, _("Account created successfully! You can now log in.")
        )
        return HttpResponseRedirect(reverse("login"))

    def form_invalid(self, form):
        if "captcha" in form.errors:
            form.errors["captcha"] = ErrorList(
                [
                    _(
                        "You must prove you are not a robot in order to register an"
                        " account. Beep boop."
                    )
                ]
            )
        return super().form_invalid(form)


class LoginView(FormView, BaseLoginView):
    body_colour = "orange"

    verb = _("Log in")
    verb_icon = "fa-user"
    breadcrumb_root = False

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get("next", reverse_lazy("dashboard"))


class LogoutView(BaseLogoutView):
    next_page = "login"
