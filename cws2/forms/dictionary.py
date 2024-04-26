from django import forms

from cws2.constants import PartOfSpeech, WordRegister
from cws2.models.dictionary import Word


class WordForm(forms.ModelForm):
    part_of_speech = forms.ChoiceField(
        choices=PartOfSpeech.CHOICES, initial=PartOfSpeech.NOUN
    )
    definition = forms.CharField(required=True)
    classes = forms.MultipleChoiceField(required=False)
    register = forms.ChoiceField(
        choices=(("", "---------"), *WordRegister.CHOICES), required=False
    )

    class Meta:
        model = Word
        fields = (
            "headword",
            "alt_word",
            "ipa",
            "xsampa",
            "part_of_speech",
            "definition",
            "register",
            "classes",
            "dialect",
            "source_language",
            "etymology",
            "notes",
            "reference_image",
        )
