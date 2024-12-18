from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from cws2.forms.user import UserProfileForm
from cws2.models.user import User
from cws2.views.base import FormView, View


class EditUserView(LoginRequiredMixin, FormView):
    form_class = UserProfileForm
    body_colour = "orange"

    page_title = _("Edit profile")
    page_icon = "bx-user-pin"

    field_classes = {"bio": "form__field--wide", "avatar": "form__field--wide"}

    @property
    def breadcrumb(self):
        return (
            (self.request.user.get_absolute_url(), f"@{self.request.user.username}"),
        )

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Your profile has been updated!"))
        return HttpResponseRedirect(form.instance.get_absolute_url())

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "instance": self.request.user}


class ShowUserView(View):
    body_colour = "orange"
    template_name = "cws2/user/show.jinja"

    page_icon = "bx-user"

    @property
    def page_title(self):
        return self.profile.username

    @property
    def breadcrumb_current(self):
        return f"@{self.profile.username}"

    @cached_property
    def profile(self):
        return get_object_or_404(User, username=self.kwargs.get("user"))

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), "profile": self.profile}
