import logging

from odoo import api, models

from lxml import etree

_logger = logging.getLogger(__name__)

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def get_arg_formatted(
        self,
        arg_name
    ):
        """Format the argument name

        The argument is stored with a dash prefix (single '-' for
        1-letter arguments and double '--' for n-letter arguments)
        """
        try:
            while(arg_name.startswith('-')):
                if(len(arg_name) <= 0):
                    break
                arg_name = arg_name[1:]
            if(len(arg_name) == 0):
                raise ValueError('Argument is of len zero')
            arg_name = '-' + arg_name
            if(len(arg_name) > 1):
                arg_name = '-' + arg_name
        except ValueError as exc:
            _logger.error(f'get_arg_formatted: {str(exc)}')
        return arg_name

    def pop_command_arg(
        self,
        args,
        arg_name,
        has_value
    ):
        """Remove entry from the command arg list (value- or flag-type)

        Keyword arguments:
        args -- The list of arguments
        arg_name -- The name of the argument to remove
        has_value -- If True the argument + value is removed, otherwise only the argument
        """
        try:
            if(not isinstance(args, list)):
                raise AssertionError('Argument list is empty')
            if(len(arg_name) == 0):
                raise AssertionError('Argument is empty')
            
            arg_name = self.get_arg_formatted(arg_name)
            if(arg_name in args):
                arg_index = args.index(arg_name)
            else:
                raise AssertionError(f'Argument {arg_name} not found in list')

            while(True):
                if(len(args) <= 0):
                    raise AssertionError('Argument list is empty')
                args.pop(arg_index)
                if(has_value):
                    has_value = False
                    continue
                break

        except AssertionError as exc:
            _logger.error(f'pop_command_arg: {str(exc)}')
        return args

    def change_command_arg(
        self,
        args,
        arg_name,
        value
    ):
        try:
            if(not isinstance(args, list)):
                raise AssertionError('Argument list is empty')
            if(len(arg_name) == 0):
                raise AssertionError('Argument is empty')
            
            arg_name = self.get_arg_formatted(arg_name)
            if(arg_name in args):
                arg_index = args.index(arg_name)
            else:
                raise AssertionError(f'Argument {arg_name} not found in list')

            value_index = arg_index + 1
            if(len(args) <= value_index):
                raise AssertionError(f'Argument list too short (probably arg with flag-type)')
            if(args[value_index].startswith('-')):
                raise AssertionError(f'Argument {arg_name} does not have a value')
            
            if(not isinstance(value, str)):
                value = str(value)
            args[value_index] = value
        except AssertionError as exc:
            _logger.error(f'pop_command_arg: {str(exc)}')
        return args

    def _prepare_html(
        self,
        html
    ):
        bodies, res_ids, header, footer, specific_paperformat_args = \
            super(IrActionsReport, self)._prepare_html(html)

        # dump items...
        #_logger.info(f'WKHTMLTOPDF: header({header.decode("utf-8")})')
        _logger.info(f'WKHTMLTOPDF: footer({footer.decode("utf-8")})')

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
        command_args = self.change_command_arg(command_args, 'zoom', '1.0')
        command_args = self.change_command_arg(command_args, 'margin-top', '32')
        command_args = self.change_command_arg(command_args, 'margin-left', '0')

        # Remove unnecessary layout elements
        #command_args = self.pop_command_arg(command_args, 'header-line', False)
        command_args = self.change_command_arg(command_args, 'header-spacing', '32')
        command_args = self.change_command_arg(command_args, 'footer-spacing', '32')

        # disable smart shrinking to allow absolute positioning and size
        # necessary for a clean din 5008 document
        command_args.extend(['--disable-smart-shrinking'])
        
        # _logger.info(f'WKHTMLTOPDF: args({", ".join(command_args)})')
        return command_args