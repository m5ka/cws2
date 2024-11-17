from django.db import IntegrityError
from django.db.models import Count
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _

from cws2.constants import GroupAccessType
from cws2.forms.group import GroupForm
from cws2.models.group import Group
from cws2.views.base import FormView, OwnableResourceMixin, View


class GroupMixin(OwnableResourceMixin):
    def get_ownable_resource(self):
        return get_object_or_404(Group, slug=self.kwargs.get("group"))


class EditGroupView(GroupMixin, FormView):
    form_class = GroupForm
    body_colour = "blue"

    ownable_permission_required = "write"

    verb_icon = "bx-edit-alt"
    field_prefixes = {"slug": "conworkshop.com/groups/"}

    @property
    def breadcrumb(self):
        return [
            (reverse("group.index"), _("Groups")),
            (self.ownable_resource.get_absolute_url(), self.ownable_resource.name),
        ]

    @property
    def verb(self):
        return _("Edit %(group)s" % {"group": self.ownable_resource.name})

    def form_valid(self, form):
        if (
            "access_type" in form.changed_data
            and form.cleaned_data.get("access_type") not in GroupAccessType.ALL_PICKABLE
        ):
            form.add_error(
                "access_type",
                ValidationError(
                    _("You cannot create a system-only group."), code="invalid"
                ),
            )
            return self.form_invalid(form)
        form.instance.updated_by = self.request.user
        try:
            form.save()
        except IntegrityError:
            return self.form_invalid(form)
        return HttpResponseRedirect(form.instance.get_absolute_url())

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "instance": self.ownable_resource}


class IndexGroupView(View):
    body_colour = "blue"
    template_name = "cws2/group/index.jinja"

    @property
    def groups(self):
        return Group.objects.order_by("name").annotate(Count("users")).all()

    def get_context_data(self, *args, **kwargs):
        return {**super().get_context_data(*args, **kwargs), "groups": self.groups}


class NewGroupView(FormView):
    form_class = GroupForm
    body_colour = "blue"

    breadcrumb = [[reverse_lazy("group.index"), _("Groups")]]
    verb = _("New group")
    verb_icon = "bx-user-plus"

    field_prefixes = {"slug": "conworkshop.com/groups/"}
    form_data = {"auto-slug-from": "name", "auto-slug": "slug"}

    def form_valid(self, form):
        if (
            "access_type" in form.changed_data
            and form.cleaned_data.get("access_type") not in GroupAccessType.ALL_PICKABLE
        ):
            form.add_error(
                "access_type",
                ValidationError(
                    _("You cannot create a system-only group."), code="invalid"
                ),
            )
            return self.form_invalid(form)
        form.instance.created_by = self.request.user
        form.instance.owned_by = self.request.user
        try:
            form.save()
        except IntegrityError:
            return self.form_invalid(form)
        return HttpResponseRedirect(form.instance.get_absolute_url())

    def get_form(self, form_class=GroupForm):
        form = form_class(**self.get_form_kwargs())
        form.fields["access_type"].choices = GroupAccessType.CHOICES_PICKABLE
        return form


class ShowGroupView(GroupMixin, View):
    template_name = "cws2/group/show.jinja"
    body_colour = "blue"

    ownable_permission_required = "read"

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "group": self.ownable_resource,
        }
