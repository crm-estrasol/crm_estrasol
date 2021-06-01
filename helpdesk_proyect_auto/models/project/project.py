from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = "project.task"
    remaining_status_sale = fields.Selection(related="sale_line_id.proyect_avaible")
    scheduled_proyect = fields.Datetime(related="sale_line_id.scheduled_proyect")
    
            



                

    