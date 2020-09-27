from odoo import api, models

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def _build_wkhtmltopdf_args(
        self,
        paperformat_id,
        landscape,
        specific_paperformat_args=None,
        set_viewport_size=False
    ):
        command_args = super(IrActionsReport, self)._build_wkhtmltopdf_args(
            paperformat_id, landscape, specific_paperformat_args=specific_paperformat_args,
            set_viewport_size=set_viewport_size)

        # disable smart shrinking to allow absolute positioning and size
        # necessary for a clean din 5008 document
        command_args.extend(['--disable-smart-shrinking'])

        return command_args