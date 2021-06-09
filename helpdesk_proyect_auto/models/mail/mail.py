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
        
        if  'model' in values:
            if 'helpdesk.ticket' == values['model']:
               
                values['is_internal'] = 0

        res = super(MailMessageCrm, self).create(values)
        
        return res
   
