# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from math import ceil

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
class MailMessageCrm(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, values):
        if  'res_model' in values:
            if 'helpdesk.ticket' in values['res_model']:
                values['is_internal'] = False
        res = super(MailMessageCrm, self).create(values)
        return res