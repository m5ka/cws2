from django import forms

from cws2.models.user import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("avatar", "pronouns", "location", "bio")
