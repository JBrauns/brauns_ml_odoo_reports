import logging

from odoo import api, models

_logger = logging.getLogger(__name__)

class IrTranslationDebug(models.Model):
  _inherit = 'ir.translation'

  @api.model
  def translate_fields(
    self,
    model,
    id,
    field=None
  ):
    field_array = field
    if(field_array is None):
      field_array = []
    _logger.info(f'ir.translation > translate_fields(model={model}' \
      ', id={id}, field={", ".join(field_array)})')

    action = super(IrTranslationDebug, self).translate_fields(self, model, id, field)

    return action