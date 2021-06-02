# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from math import ceil

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'


    @api.depends('team_id')
    def _compute_project_id(self):
        for ticket in self:
            pass

    