from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from cws2.forms.translation import TranslationForm, TranslationTemplateForm
from cws2.models.translation import TranslationTemplate
from cws2.views.base import FormView, View


class IndexTranslationTemplateView(LoginRequiredMixin, View):
    template_name = "cws2/translation/index.jinja"

    page_title = _("Translations")
    page_icon = "bx-transfer"

    def get_context_data(self, **kwargs):
        translation_templates = TranslationTemplate.objects.annotate(
            translation_count=Count("translations")
        ).all()
        return {
            **super().get_context_data(**kwargs),
            "translation_templates": translation_templates,
        }


class NewTranslationTemplateView(LoginRequiredMixin, FormView):
    form_class = TranslationTemplateForm

    page_title = _("New translation")
    page_icon = "bx-plus"

    breadcrumb = ((reverse_lazy("translation.index"), _("Translations")),)

    field_classes = {"name": "form__field--wide", "text": "form__field--wide"}

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        return redirect(
            reverse("translation.show", kwargs={"translation": form.instance.uuid})
        )


class NewTranslationView(LoginRequiredMixin, FormView):
    form_class = TranslationForm


class ShowTranslationTemplateView(LoginRequiredMixin, View):
    template_name = "cws2/translation/show.jinja"

    page_icon = "bx-transfer"

    @property
    def breadcrumb(self):
        return ((reverse("translation.index"), _("Translations")),)

    @cached_property
    def translation_template(self):
        return get_object_or_404(
            TranslationTemplate.objects.prefetch_related("translations"),
            uuid=self.kwargs.get("translation"),
        )

    @property
    def page_title(self):
        return self.translation_template.name

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "translation_template": self.translation_template,
        }
