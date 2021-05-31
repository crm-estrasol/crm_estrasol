# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _

class packlifewarehouse(models.Model):
    _inherit  = 'res.partner'
    x_warehouse_especial = fields.Many2one('stock.warehouse')
    