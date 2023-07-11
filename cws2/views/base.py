from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import generic


class View(generic.TemplateView):
    template_name = "cws2/base.jinja"
    body_colour = "green"

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "body_colour": self.body_colour,
        }


class FormView(View, generic.FormView):
    template_name = "cws2/form.jinja"

    verb = "Submit form"
    verb_icon = "fa-rocket"
    breadcrumb = []
    breadcrumb_root = True

    field_classes = {}
    field_prefixes = {}
    hidden_fields = {}
    form_data = {}

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "verb": self.verb,
            "verb_icon": self.verb_icon,
            "breadcrumb": self.breadcrumb,
            "breadcrumb_root": self.breadcrumb_root,
            "field_classes": self.field_classes,
            "field_prefixes": self.field_prefixes,
            "hidden_fields": self.hidden_fields,
            "form_data": self.form_data,
        }


class OwnableResourceMixin:
    """Contains useful functionality for views that deal with Ownable resources, such
    as automatically managing the permissions required to view the resource and
    automatically caching the resource as an attribute of the view.

    Example:
        ```
        class MyView(OwnableResourceView, FormView):
            ownable_permission_required = "write"

            def get_ownable_resource(self):
                return Resource.objects.get(slug=self.kwargs.get("resource"))
        ```
    """

    @property
    def ownable_permission_required(self):
        """The required permission needed on this Ownable resource to do what is being
        done in this view.

        Override this in child classes by setting `ownable_permission_required` as a
        class variable.

        Example:
            ```
            ownable_permission_required = "write"
            ```
        """
        raise ImproperlyConfigured(
            f"{self.__class__.__name__} inherits from OwnableMixin and must define "
            "ownable_permission_required."
        )

    @property
    def ownable_resource(self):
        """A cached copy of this view's ownable resource."""
        if not hasattr(self, "_ownable_resource") or not self._ownable_resource:
            self._ownable_resource = self.get_ownable_resource()
        return self._ownable_resource

    def get_ownable_resource(self):
        """A function used to fetch this view's ownable resource.

        Override this in child classes with the code required to fetch the ownable
        resource.

        Example:
            ```
            def get_ownable_resource(self):
                return Resource.objects.get(slug=self.kwargs.get("resource"))
            ```
        """
        raise ImproperlyConfigured(
            f"{self.__class__.__name__} inherits from OwnableMixin and must define "
            "get_ownable_resource()."
        )

    def handle_ownable_forbidden(self, request):
        """This function is called if the user does not have the required permissions
        to interact with this ownable resource.
        """
        if not self.request.user.is_authenticated:
            messages.warning(request, _("Try logging in before trying to access that!"))
            return HttpResponseRedirect(reverse("login"))
        if (
            self.ownable_permission_required != "read"
            and self.ownable_resource.is_public
        ):
            messages.warning(
                request, _("You don't have the required permissions to do that.")
            )
            return HttpResponseRedirect(self.ownable_resource.get_absolute_url())
        messages.warning(
            request,
            _("You don't have the required permissions to view that resource."),
        )
        return HttpResponseRedirect(reverse("dashboard"))

    def dispatch(self, request, *args, **kwargs):
        if not self.ownable_resource.check_user_permission(
            request.user, self.ownable_permission_required
        ):
            return self.handle_ownable_forbidden(request)
        return super().dispatch(request, *args, **kwargs)
