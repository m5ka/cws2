from django.shortcuts import get_object_or_404

from cws2.models.user import User
from cws2.views.base import View


class ShowUserView(View):
    body_colour = "orange"
    template_name = "cws2/user/show.jinja"

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "this_user": get_object_or_404(User, username=self.kwargs.get("user")),
        }
