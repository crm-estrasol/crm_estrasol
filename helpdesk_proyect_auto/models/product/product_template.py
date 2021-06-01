    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class packlifeproduct(models.Model):
    _inherit = 'product.template'
    brand = fields.Char('Marca')
    

class packlifeproduct2(models.Model):
    _inherit = 'product.product'
    brand = fields.Char('Marca')
    standard_price = fields.Float(
        'Cost', company_dependent=True,
        digits='Product Price',
        groups="base.group_user",
        tracking=True,
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
        In FIFO: value of the last unit that left the stock (automatically computed).
        Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
        Used to compute margins on sale orders.""")