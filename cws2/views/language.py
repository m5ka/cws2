from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from cws2.forms.language import LanguageForm
from cws2.models.language import Language
from cws2.views.base import FormView, OwnableResourceMixin, View


class LanguageMixin(OwnableResourceMixin):
    def get_ownable_resource(self):
        return get_object_or_404(
            Language.objects.select_related("owned_by"),
            owned_by__username=self.kwargs.get("user"),
            slug=self.kwargs.get("language"),
        )


class EditLanguageView(LanguageMixin, FormView):
    form_class = LanguageForm

    ownable_permission_required = "write"

    page_icon = "bx-edit-alt"
    field_classes = {"description": "form__field--wide"}
    form_data = {"auto-slug-from": "name", "auto-slug": "slug"}

    @property
    def breadcrumb(self):
        return (
            (
                self.ownable_resource.created_by.get_absolute_url(),
                f"@{self.ownable_resource.created_by.username}",
            ),
            (self.ownable_resource.get_absolute_url(), self.ownable_resource.name),
        )

    @property
    def page_title(self):
        return _("Edit %(language)s") % {"language": self.ownable_resource.name}

    @property
    def field_prefixes(self):
        return {
            "slug": "conworkshop.com/@%s/" % (self.ownable_resource.owned_by.username)
        }

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        try:
            form.save()
        except IntegrityError:
            return self.form_invalid(form)
        messages.success(self.request, _("Language updated successfully!"))
        return HttpResponseRedirect(form.instance.get_absolute_url())

    def get_form(self):
        return self.form_class(instance=self.ownable_resource, **self.get_form_kwargs())


class IndexLanguageView(LoginRequiredMixin, View):
    template_name = "cws2/language/index.jinja"

    page_title = _("My languages")
    breadcrumb_current = _("Languages")
    page_icon = "bx-book"

    @cached_property
    def languages(self):
        return Language.objects.filter(owned_by=self.request.user)

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), "languages": self.languages}


class NewLanguageView(LoginRequiredMixin, FormView):
    form_class = LanguageForm

    page_title = _("New language")
    page_icon = "bx-book-add"
    breadcrumb = ((reverse_lazy("language.index"), _("Languages")),)
    field_classes = {"description": "form__field--wide"}
    form_data = {"auto-slug-from": "name", "auto-slug": "slug"}

    @property
    def field_prefixes(self):
        return {"slug": f"conworkshop.com/@{self.request.user.username}/"}

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.owned_by = self.request.user
        try:
            form.save()
        except IntegrityError:
            return self.form_invalid(form)
        messages.success(self.request, _("Language created successfully!"))
        return HttpResponseRedirect(form.instance.get_absolute_url())


class ShowLanguageView(LanguageMixin, View):
    template_name = "cws2/language/show.jinja"

    ownable_permission_required = "read"

    @property
    def breadcrumb(self):
        return (
            (
                self.ownable_resource.created_by.get_absolute_url(),
                f"@{self.ownable_resource.created_by.username}",
            ),
        )

    @property
    def page_title(self):
        return self.ownable_resource.name

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), "language": self.ownable_resource}
