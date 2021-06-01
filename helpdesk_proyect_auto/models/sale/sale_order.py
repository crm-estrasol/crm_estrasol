from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    scheduled_proyect = fields.Datetime(string="Fecha limite proyecto")
    proyect_avaible = fields.Char('Estado proyecto', copy=False, compute='_compute_proyect_available', compute_sudo=True, store=True, digits='Product Unit of Measure', default="No aplica")

    #OVERRIDE
    @api.depends('product_id.service_policy')
    def _compute_remaining_hours_available(self):
        uom_hour = self.env.ref('uom.product_uom_hour')
        for line in self:
            #this was override due to consider remaining hour must include timesheet hour 
            is_ordered_timesheet = line.product_id.service_policy in  ['ordered_timesheet' ,'delivered_timesheet']
            is_time_product = line.product_uom.category_id == uom_hour.category_id
            line.remaining_hours_available = is_ordered_timesheet and is_time_product
  
    @api.depends('qty_delivered')
    def _compute_proyect_available(self):
        uom_hour = self.env.ref('uom.product_uom_hour')
        for line in self:
            if  line.project_id or line.task_id:
                uom_hour = self.env.ref('uom.product_uom_hour')
                is_time_product = line.product_uom.category_id == uom_hour.category_id
                if is_time_product :
                    #has due date
                    if line.scheduled_proyect :
                        if line.scheduled_proyect > fields.Datetime.today(): 
                                line.proyect_avaible = "Vencio"
                        else:
                            if line.qty_delivered >= line.qty_ordered:
                                line.proyect_avaible = "Vencio"
                            else:
                                 line.proyect_avaible = "Vigente"
                    #has time
                    else:
                            if line.qty_delivered >= line.qty_ordered:
                                line.proyect_avaible = "Vencio"
                            else:
                
                                 line.proyect_avaible = "Vigente"                
                #no time but due date
                else:
                     if line.scheduled_proyect:
                            if line.scheduled_proyect > fields.Datetime.today(): 
                                line.proyect_avaible = "Vencio"
                            else:
                                line.proyect_avaible = "Vigente"
               
                



                

    