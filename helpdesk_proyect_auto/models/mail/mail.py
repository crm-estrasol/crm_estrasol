# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from math import ceil

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
class MailMessageCrm(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, values):
        if  'res_model' in values:
            if 'helpdesk.ticket' == values['res_model']:
                _logger.info("3333333333333333333333333")
                _logger.info(values['res_model'])
                values['is_internal'] = 0

        res = super(MailMessageCrm, self).create(values)
        
        return res
   
