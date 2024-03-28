from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from cws2.models.user import User, UserProfile
from cws2.views.base import FormView, View


class UserForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["pronouns", "location", "bio"]


class EditUserView(LoginRequiredMixin, FormView):
    form_class = UserForm
    body_colour = "orange"

    verb = _("Edit profile")
    verb_icon = "fa-user-pen"

    field_classes = {"bio": "form__field--wide"}

    @property
    def breadcrumb(self):
        return [
            [self.request.user.get_absolute_url(), f"@{self.request.user.username}"]
        ]

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Your profile has been updated!"))
        return HttpResponseRedirect(form.instance.user.get_absolute_url())

    def get_form(self):
        return self.form_class(
            instance=self.request.user.profile, **self.get_form_kwargs()
        )


class ShowUserView(View):
    body_colour = "orange"
    template_name = "cws2/user/show.jinja"

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "this_user": get_object_or_404(User, username=self.kwargs.get("user")),
        }
