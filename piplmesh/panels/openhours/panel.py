from django.utils.translation import ugettext_lazy as _

from piplmesh import panels
from piplmesh.panels.map import panel as map_panel

class OpenHoursPanel(panels.BasePanel):
    dependencies = (map_panel.MapPanel.get_name(),)

    def get_context(self, context):
        context.update({
            'header': _("OpenHours"),
        })
        return context

panels.panels_pool.register(OpenHoursPanel)
