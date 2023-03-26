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
