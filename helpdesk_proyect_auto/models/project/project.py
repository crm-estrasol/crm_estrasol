from odoo import models, fields, api, _
from odoo.exceptions import UserError
class FlexiProject(models.Model):
    _inherit = "project.project"
     project_stage = fields.Selection([('none','No aplica'),('process','En proceso'),('production','Produccion')],string="Estatus proyecto", tracking=True,) 
class ProjectTask(models.Model):
    _inherit = "project.task"
    remaining_status_sale = fields.Selection(related="sale_line_id.proyect_avaible")
    scheduled_proyect = fields.Date(related="sale_line_id.scheduled_proyect")
   
            
class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'
    is_start = fields.Boolean('Paused', help="")


                

    