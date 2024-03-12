from cws2.models.message import Message
from cws2.views.base import View


class IndexMessageView(View):
    template_name = "cws2/message/index.jinja"
    body_colour = "orange"
