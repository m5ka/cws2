from cws2.views.base import View


class AboutView(View):
    body_colour = "blue"
    template_name = "cws2/static/about.jinja"


class ContactView(View):
    body_colour = "orange"
    template_name = "cws2/static/contact.jinja"


class DonateView(View):
    body_colour = "orange"
    template_name = "cws2/static/donate.jinja"


class PrivacyView(View):
    body_colour = "orange"
    template_name = "cws2/static/privacy.jinja"
