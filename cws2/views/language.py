from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from cws2.models.language import Language
from cws2.views.base import FormView, View


class IndexLanguageView(LoginRequiredMixin, View):
    template_name = "cws2/language/index.jinja"

    @cached_property
    def languages(self):
        return Language.objects.filter(created_by=self.request.user)

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "languages": self.languages,
        }


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = [
            "name",
            "endonym",
            "slug",
            "language_type",
            "language_status",
            "description",
        ]


class NewLanguageView(LoginRequiredMixin, FormView):
    form_class = LanguageForm

    verb = _("New language")
    verb_icon = "fa-plus"
    breadcrumb = [[reverse_lazy("language.index"), _("Languages")]]

    field_classes = {
        "slug": "span-two",
        "description": "span-two",
    }
    form_data = {
        "auto-slug-from": "name",
        "auto-slug": "slug",
    }

    @property
    def field_prefixes(self):
        return {"slug": "conworkshop.com/@%s/" % (self.request.user.username)}

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.owned_by = self.request.user
        form.save()
        messages.success(self.request, _("Language created successfully!"))
        return HttpResponseRedirect(form.instance.get_absolute_url())


class ShowLanguageView(View):
    template_name = "cws2/language/show.jinja"

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "language": get_object_or_404(
                Language,
                created_by__username=self.kwargs.get("user"),
                slug=self.kwargs.get("language"),
            ),
        }
