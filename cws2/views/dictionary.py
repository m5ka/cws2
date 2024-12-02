from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from cws2.forms.dictionary import NewWordForm, WordForm
from cws2.models.dictionary import Word, WordClass, WordDefinition
from cws2.models.language import Language
from cws2.views.base import FormView, OwnableResourceMixin, View


class EditWordView(LoginRequiredMixin, OwnableResourceMixin, FormView):
    form_class = WordForm
    template_name = "cws2/dictionary/edit.jinja"

    page_icon = "bx-edit-alt"

    ownable_permission_required = "write"

    @property
    def breadcrumb(self):
        return [
            (
                self.word.language.created_by.get_absolute_url(),
                f"@{self.word.language.created_by.username}",
            ),
            (self.word.language.get_absolute_url(), self.word.language.name),
            (
                reverse(
                    "word.index",
                    kwargs={
                        "user": self.word.language.created_by.username,
                        "language": self.word.language.slug,
                    },
                ),
                _("Dictionary"),
            ),
            (self.word.get_absolute_url(), self.word.headword),
        ]

    @property
    def page_title(self):
        return _("Edit %(word)s") % {"word": self.word.headword}

    @cached_property
    def word(self):
        return get_object_or_404(
            Word.objects.select_related("language__created_by"),
            language=self.ownable_resource,
            uuid=self.kwargs.get("word"),
        )

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        form.save()
        messages.success(self.request, _("Word updated successfully!"))
        return redirect(form.instance.get_absolute_url())

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "instance": self.word}

    def get_ownable_resource(self):
        return get_object_or_404(
            Language,
            slug=self.kwargs.get("language"),
            created_by__username=self.kwargs.get("user"),
        )


class IndexWordView(OwnableResourceMixin, View):
    template_name = "cws2/dictionary/index.jinja"

    page_icon = "bx-text"
    breadcrumb_current = _("Dictionary")

    ownable_permission_required = "read"

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
        return _("%(language)s dictionary") % {"language": self.ownable_resource.name}

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
    form_class = NewWordForm
    template_name = "cws2/dictionary/new.jinja"

    page_title = _("New word")
    page_icon = "bx-message-alt-add"

    ownable_permission_required = "write"

    @property
    def breadcrumb(self):
        return [
            (
                self.ownable_resource.created_by.get_absolute_url(),
                f"@{self.ownable_resource.created_by.username}",
            ),
            (self.ownable_resource.get_absolute_url(), self.ownable_resource.name),
            (
                reverse(
                    "word.index",
                    kwargs={
                        "user": self.ownable_resource.created_by.username,
                        "language": self.ownable_resource.slug,
                    },
                ),
                _("Dictionary"),
            ),
        ]

    def form_valid(self, form):
        form.instance.language = self.ownable_resource
        form.instance.created_by = self.request.user
        with transaction.atomic():
            form.save()
            definition = WordDefinition.objects.create(
                word=form.instance,
                part_of_speech=form.cleaned_data.get("part_of_speech"),
                definition=form.cleaned_data.get("definition"),
                register=form.cleaned_data.get("register"),
            )
            definition.classes.set(form.cleaned_data.get("classes"))
        messages.success(self.request, _("Word created successfully!"))
        return redirect(form.instance.get_absolute_url())

    def get_form(self, form_class=None):
        if not form_class:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        classes = WordClass.objects.filter(language=self.ownable_resource).all()
        form.fields["classes"].choices = ((c.id, c.label) for c in classes)
        return form

    def get_ownable_resource(self):
        return get_object_or_404(
            Language,
            slug=self.kwargs.get("language"),
            created_by__username=self.kwargs.get("user"),
        )


class ShowWordView(View):
    template_name = "cws2/dictionary/show.jinja"

    @property
    def page_title(self):
        return self.word.headword

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "word": self.word,
            "editable": self.word.language.check_user_permission(
                self.request.user, "write"
            ),
        }

    @cached_property
    def word(self):
        return get_object_or_404(
            Word.objects.select_related("language__created_by"),
            language__created_by__username=self.kwargs.get("user"),
            language__slug=self.kwargs.get("language"),
            uuid=self.kwargs.get("word"),
        )
