from django import forms

from cws2.models.translation import Translation, TranslationTemplate


class TranslationTemplateForm(forms.ModelForm):
    class Meta:
        model = TranslationTemplate
        fields = ("name", "text", "description", "source")


class TranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ("translation", "is_wip")
