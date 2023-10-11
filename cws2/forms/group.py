from django.forms import ModelForm

from cws2.models.group import Group


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = [
            "name",
            "slug",
            "icon",
            "icon_colour_bg",
            "icon_colour_fg",
            "access_type",
        ]
