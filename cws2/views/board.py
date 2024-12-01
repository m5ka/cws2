from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Case, Count, IntegerField, Prefetch, When
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cws2.constants import GroupAccessType
from cws2.forms.board import BoardForm
from cws2.models.board import Board
from cws2.models.group import Group
from cws2.views.base import FormView, OwnableResourceMixin, View


class IndexBoardView(View):
    template_name = "cws2/board/index.jinja"
    body_colour = "blue"

    page_title = _("Boards")
    page_icon = "bx-conversation"

    def get_context_data(self, **kwargs):
        board_prefetch = Prefetch("boards", queryset=Board.objects.order_by("name"))
        is_system_case = Case(
            When(access_type=GroupAccessType.SYSTEM, then=1),
            default=0,
            output_field=IntegerField(),
        )
        groups = (
            Group.objects.annotate(
                is_system=is_system_case, board_count=Count("boards")
            )
            .filter(users__user=self.request.user, board_count__gt=0)
            .order_by("-is_system", "name")
            .prefetch_related(board_prefetch)
            .all()
        )
        return {**super().get_context_data(**kwargs), "groups": groups}


class NewBoardView(OwnableResourceMixin, FormView):
    form_class = BoardForm

    page_title = _("New Board")
    page_icon = "bx-message-alt-add"
    body_colour = "blue"
    form_data = {"auto-slug-from": "name", "auto-slug": "slug"}

    ownable_permission_required = "write"

    @property
    def breadcrumb(self):
        return (
            (reverse("group.index"), _("Groups")),
            (self.ownable_resource.get_absolute_url(), self.ownable_resource.name),
        )

    @property
    def field_prefixes(self):
        return {"slug": f"conworkshop.com/groups/{self.ownable_resource.slug}/"}

    def get_ownable_resource(self):
        return get_object_or_404(Group, slug=self.kwargs.get("group"))

    def form_valid(self, form):
        form.instance.group = self.ownable_resource
        try:
            form.save()
        except IntegrityError:
            return self.form_invalid(form)
        messages.success(self.request, _("Board created successfully!"))
        return HttpResponseRedirect(self.ownable_resource.get_absolute_url())


class ShowBoardView(View):
    pass
