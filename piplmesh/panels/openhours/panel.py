from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

class OpenHoursPanel(panels.BasePanel):
    def get_context(self, context):
        context.update({
            'header': _("OpenHours"),
        })
        return context

panels.panels_pool.register(OpenHoursPanel)
