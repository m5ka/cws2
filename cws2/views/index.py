from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from cws2.views.base import View


class DashboardView(LoginRequiredMixin, View):
    body_colour = "blue"
    template_name = "cws2/dashboard.jinja"

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse("about"))
