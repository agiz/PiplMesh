from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

class OdpiralniCasiPanel(panels.BasePanel):
    def get_context(self, context):
        context.update({
            'header': _("OdpiralniCasi"),
        })
        return context

panels.panels_pool.register(OdpiralniCasiPanel)
