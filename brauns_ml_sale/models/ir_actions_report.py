import logging

from odoo import api, models

from lxml import etree

_logger = logging.getLogger(__name__)

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def pop_command_arg(
        self,
        args,
        arg_name,
        has_value
    ):
        # allowed arg_types:
        #   flag - Simple argument prefixed with a single or double '-' without a value
        #   path - Argument with a path given as the value
        #   
        if(not isinstance(args, list)):
            _logger.error(f'WKHTMLTOPDF: Argument list is empty')
            return args
        if(len(arg_name) == 0):
            _logger.error(f'WKHTMLTOPDF: Argument is empty')
            return args
        
        # 1. remove possible dashes
        # 2. add back dashes based on the length of the argument (l=1 or l>1)
        while(arg_name.startswith('-')):
            arg_name = arg_name[1:]
        if(len(arg_name) == 0):
            _logger.error(f'WKHTMLTOPDF: Argument is empty')
            return args
        arg_name = '-' + arg_name
        if(len(arg_name) > 1):
            arg_name = '-' + arg_name
        
        # 1. get the argument index
        # 2. remove the argument [remove the value]
        try:
            arg_index = args.index(arg_name)
        except ValueError:
            _logger.warning(f'WKHTMLTOPDF: Argument "{arg_name}" not found')
            return args

        while(True):
            try:
                args.pop(arg_index)
            except IndexError:
                _logger.error(f'WKHTMLTOPDF: Argument list is empty')
                return args
            if(has_value):
                has_value = False
                continue
            break

        return args

    def _prepare_html(
        self,
        html
    ):
        bodies, res_ids, header, footer, specific_paperformat_args = \
            super(IrActionsReport, self)._prepare_html(html)

        # dump items...
        _logger.info(f'WKHTMLTOPDF: header({etree.tostring(header, pretty_print=True).decode("utf-8")})')
        _logger.info(f'WKHTMLTOPDF: footer({etree.tostring(footer, pretty_print=True).decode("utf-8")})')

        return bodies, res_ids, header, footer, specific_paperformat_args

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

        # The way the zoom argument is used within the dpí cal
        command_args = self.pop_command_arg(command_args, 'zoom', True)
        command_args.extend(['--zoom', '1.0'])

        # Remove unnecessary layout elements
        command_args = self.pop_command_arg(command_args, 'header-line', False)

        # disable smart shrinking to allow absolute positioning and size
        # necessary for a clean din 5008 document
        command_args.extend(['--disable-smart-shrinking'])
        
        _logger.info(f'WKHTMLTOPDF: args({", ".join(command_args)})')
        return command_args