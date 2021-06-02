from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    scheduled_proyect = fields.Date(string="Fecha limite proyecto", default=lambda self: fields.Date.today())
    proyect_avaible =fields.Selection([
        ('none', 'No aplica'),
        ('active', 'Disponible'),
        ('off', 'Vencio')],
        copy=False, compute='_compute_proyect_available', compute_sudo=True, store=True, 
        string="Estatus proyecto",
        digits='Product Unit of Measure', default="none")
    
    #OVERRIDE
    @api.depends('product_id.service_policy')
    def _compute_remaining_hours_available(self):
        uom_hour = self.env.ref('uom.product_uom_hour')
        for line in self:
            #this was override due to consider remaining hour must include timesheet hour 
            is_ordered_timesheet = line.product_id.service_policy in  ['ordered_timesheet' ,'delivered_timesheet']
            is_time_product = line.product_uom.category_id == uom_hour.category_id
            line.remaining_hours_available = is_ordered_timesheet and is_time_product
  
    
    def refresh_all_states(self):
        items = self.env['sale.order.line'].search([])
        
        
        for r in items.filtered(lambda move: move.product_id.type == 'service'):
                if r.scheduled_proyect:
                            if r.scheduled_proyect > fields.Date.today(): 
                                r.proyect_avaible = "off"
                            else:
                                r.proyect_avaible = "active"
                else:
                    r.proyect_avaible = "none"

    @api.depends('qty_delivered','order_id.state')
    def _compute_proyect_available(self):
        uom_hour = self.env.ref('uom.product_uom_hour')
        for line in self:
            if  line.project_id or line.task_id:
                uom_hour = self.env.ref('uom.product_uom_hour')
                is_time_product = line.product_uom.category_id == uom_hour.category_id
                if is_time_product :
                    #has due date
                    if line.scheduled_proyect :
                        if line.scheduled_proyect > fields.Date.today(): 
                                line.proyect_avaible = "off"
                        else:
                            if line.qty_delivered >= line.product_uom_qty:
                                line.proyect_avaible = "off"
                            else:
                                 line.proyect_avaible = "active"
                    #has time
                    else:
                            if line.qty_delivered >= line.product_uom_qty:
                                line.proyect_avaible = "off"
                            else:
                
                                 line.proyect_avaible = "active"                
                #no time but due date
                else:
                    if line.scheduled_proyect:
                            if line.scheduled_proyect > fields.Date.today(): 
                                line.proyect_avaible = "off"
                            else:
                                line.proyect_avaible = "active"
                    else:
                        line.proyect_avaible = "none"
               
            



                

    