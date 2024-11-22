from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext as _
from PIL import Image

from cws2.forms.widgets import ClearableImageInput
from cws2.images import process_flag_image
from cws2.models.language import Language


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = [
            "name",
            "endonym",
            "slug",
            "language_flag",
            "language_type",
            "language_status",
            "description",
        ]
        widgets = {"language_flag": ClearableImageInput}

    def clean_language_flag(self):
        flag = self.cleaned_data["language_flag"]
        if "language_flag" in self.changed_data and flag:
            image = Image.open(flag)
            width, height = image.size
            if width < 100 or height < 50:
                raise ValidationError(
                    _(
                        "Flag image is too small. It must be at least 100px wide and "
                        "50px high."
                    ),
                    code="invalid",
                )
            return process_flag_image(image)
        return flag
