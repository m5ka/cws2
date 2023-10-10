from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext as _
from PIL import Image

from cws2.forms.widgets import ClearableImageInput
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["language_flag"].widget = ClearableImageInput()

    def clean_language_flag(self):
        flag = self.cleaned_data["language_flag"]
        if flag:
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
            name = ".".join(flag.name.split(".")[:-1]) + ".webp"
            image.thumbnail((100, 100))
            buffer = BytesIO()
            image.save(buffer, "webp")
            return InMemoryUploadedFile(
                buffer,
                "ImageField",
                name,
                "image/webp",
                buffer.getbuffer().nbytes,
                None,
            )
        return flag
