from django.forms import ModelForm

from cws2.models.board import Board


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ("name", "slug")
