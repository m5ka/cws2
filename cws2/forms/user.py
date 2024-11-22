from django import forms

from cws2.forms.widgets import ClearableImageInput
from cws2.images import process_avatar_image
from cws2.models.user import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("avatar", "pronouns", "location", "bio")
        widgets = {"avatar": ClearableImageInput}

    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]
        if "avatar" in self.changed_data and avatar:
            return process_avatar_image(avatar)
        return avatar
