from django.forms.widgets import ClearableFileInput


class ClearableImageInput(ClearableFileInput):
    template_name = "cws2/widgets/clearable_image_input.jinja"
