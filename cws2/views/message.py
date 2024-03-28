from cws2.models.message import Message
from cws2.views.base import View


class IndexMessageView(View):
    template_name = "cws2/message/index.jinja"
    body_colour = "orange"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "messages": (
                Message.objects.filter(recipient=self.request.user)
                .order_by("recipient", "-created_at").distinct("recipient")
            ),
        }
