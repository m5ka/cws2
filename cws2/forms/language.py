from django.forms import ModelForm

from cws2.models.language import Language


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
