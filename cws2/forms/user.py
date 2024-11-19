from django import forms
from django.utils.translation import gettext_lazy as _

from cws2.models.user import User, UserProfile


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label=_("Avatar"), required=False)

    class Meta:
        model = UserProfile
        fields = ("avatar", "pronouns", "location", "bio")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].help_text = User._meta.get_field("avatar").help_text
