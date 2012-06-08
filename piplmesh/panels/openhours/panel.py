from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

class OpenhoursPanel(panels.BasePanel):
    def get_context(self, context):
        context.update({
            'header': _("Openhours"),
        })
        return context

panels.panels_pool.register(OpenhoursPanel)
