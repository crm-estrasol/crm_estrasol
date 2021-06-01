from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #OVERRIDE
    @api.depends('product_id.service_policy')
    def _compute_remaining_hours_available(self):
        uom_hour = self.env.ref('uom.product_uom_hour')
        for line in self:
            #this was override due to consider remaining hour must include timesheet hour 
            is_ordered_timesheet = line.product_id.service_policy in  ['ordered_timesheet' ,'delivered_timesheet']
            is_time_product = line.product_uom.category_id == uom_hour.category_id
            line.remaining_hours_available = is_ordered_timesheet and is_time_product
  





    