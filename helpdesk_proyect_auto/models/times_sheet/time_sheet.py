# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree
import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'


    def _timesheet_get_portal_domain(self):
        if self.env.user.has_group('base.group_portal') and self.env.user.partner_id.parent_id:
            return [
                    ('task_id.partner_id', '=', self.env.user.partner_id.parent_id.id )
                ]
        res = super(AccountAnalyticLine, self)._timesheet_get_portal_domain(self)
        
        return res