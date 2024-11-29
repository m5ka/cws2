from django.utils.translation import gettext_lazy as _

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
    page_title = _("Donate to ConWorkShop")
    page_icon = "bx-gift"


class PrivacyView(View):
    body_colour = "orange"
    template_name = "cws2/static/privacy.jinja"
    page_title = _("Privacy Policy")
    page_icon = "bx-check-shield"
