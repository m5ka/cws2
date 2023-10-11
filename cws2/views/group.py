from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from cws2.forms.group import GroupForm
from cws2.models.group import Group
from cws2.views.base import FormView, View, OwnableResourceMixin


class GroupMixin(OwnableResourceMixin):
    def get_ownable_resource(self):
        return get_object_or_404(
            Group,
            slug=self.kwargs.get("group"),
        )


class EditGroupView(GroupMixin, FormView):
    form_class = GroupForm
    body_colour = "blue"

    ownable_permission_required = "write"

    verb_icon = "fa-house-user"

    @property
    def verb(self):
        return _("Edit %(group)s" % {"group": self.ownable_resource.name})


class IndexGroupView(View):
    body_colour = "blue"
    template_name = "cws2/group/index.jinja"

    @property
    def groups(self):
        return Group.objects.order_by("name").annotate(Count("users")).all()

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "groups": self.groups,
        }


class NewGroupView(FormView):
    form_class = GroupForm
    body_colour = "blue"

    breadcrumb = [[reverse_lazy("group.index"), _("Groups")]]
    verb = _("New group")
    verb_icon = "fa-house-user"

    field_prefixes = {"slug": "conworkshop.com/groups/"}
    form_data = {
        "auto-slug-from": "name",
        "auto-slug": "slug",
    }


class ShowGroupView(GroupMixin, View):
    template_name = "cws2/group/show.jinja"
    body_colour = "blue"

    ownable_permission_required = "read"

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "group": self.ownable_resource,
        }
