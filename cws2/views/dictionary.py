from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from cws2.forms.dictionary import WordForm
from cws2.models.dictionary import Word, WordDefinition
from cws2.models.language import Language
from cws2.views.base import FormView, OwnableResourceMixin, View


class IndexWordView(OwnableResourceMixin, View):
    template_name = "cws2/dictionary/index.jinja"

    ownable_permission_required = "read"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "language": self.ownable_resource,
            "words": Word.objects.filter(language=self.ownable_resource).all(),
        }

    def get_ownable_resource(self):
        return get_object_or_404(
            Language,
            created_by__username=self.kwargs.get("user"),
            slug=self.kwargs.get("language"),
        )


class NewWordView(LoginRequiredMixin, OwnableResourceMixin, FormView):
    form_class = WordForm

    verb = "New word"
    verb_icon = "fa-text"

    ownable_permission_required = "write"

    @property
    def breadcrumb(self):
        return [
            (
                reverse(
                    "user.show",
                    kwargs={"user": self.ownable_resource.created_by.username},
                ),
                f"@{self.ownable_resource.created_by.username}"
            ),
            (
                reverse(
                    "language.show",
                    kwargs={
                        "user": self.ownable_resource.created_by.username,
                        "language": self.ownable_resource.slug,
                    }
                ),
                self.ownable_resource.name,
            ),
        ]

    def form_valid(self, form):
        form.instance.language = self.ownable_resource
        with transaction.atomic():
            form.save()
            WordDefinition.objects.create(
                word=form.instance,
                part_of_speech=form.cleaned_data.get("part_of_speech"),
                definition=form.cleaned_data.get("definition"),
                register=form.cleaned_data.get("register"),
            )
        messages.success(self.request, _("Word created successfully!"))
        return redirect(form.instance.get_absolute_url())

    def get_form(self):
        # TODO: populate word class choices here!
        return self.form_class(**self.get_form_kwargs())

    def get_ownable_resource(self):
        return get_object_or_404(
            Language,
            slug=self.kwargs.get("language"),
            created_by__username=self.kwargs.get("user"),
        )


class ShowWordView(View):
    template_name = "cws2/dictionary/show.jinja"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "word": self.word,
        }

    @cached_property
    def word(self):
        return get_object_or_404(
            Word.objects.select_related("language__created_by"),
            language__created_by__username=self.kwargs.get("user"),
            language__slug=self.kwargs.get("language"),
            uuid=self.kwargs.get("word"),
        )
