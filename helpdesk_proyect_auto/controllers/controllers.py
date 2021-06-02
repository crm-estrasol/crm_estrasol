
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import ValidationError
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers.main import Website
from odoo.osv import expression
_logger = logging.getLogger(__name__)
import base64
from odoo.tools import ImageProcess
import werkzeug
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
from odoo import http
from odoo.http import request
#from enterpise.y.controllers.main import WebsiteForm
from odoo.addons.website_helpdesk_form.controller.main import WebsiteForm

class WebsiteTicketValidation(http.Controller):
    @http.route(['/mesa-de-ayuda'], type='http', auth="user", website=True)
    def create_icket(self, **kw):
        id_user = request.env.user.id
        user = request.env['res.users'].browse(id_user).partner_id.parent_id
        
        items_status = []
        for so  in request.env['sale.order.line'].sudo().search( [ ('order_id.partner_id','=',user.id),('order_id.partner_id.is_company','=',True) ] ):    
            if so.proyect_avaible == 'active': 
                if so.task_id: 
                    if  so.task_id.stage_id.is_start:
                        continue
                    if  so.task_id.stage_id.is_closed : 
                        continue
                    items_status.append([so.task_id,so.task_id.project_id])        
                   
                items_p = request.env['project.task'].sudo().search([ ('project_id','=', so.project_id.id)  ])
                if items_p:
                    looked = items_p.filtered( lambda x:  x.stage_id.is_start == False     )
                    looked = looked.filtered( lambda x:  x.stage_id.is_closed == False    ) 
                    if looked:
                        items_status.append([looked[0], looked[0].project_id ] )
                        
        #items = list(set( [i for i in items] ))                     
        #items_status = list(set( [i for i in items_status] ))
        
        if items_p:
            return request.render('helpdesk_proyect_auto.mesa_ayuda',{'proys_status':items_status,'user_email':request.env.user.email})
        else:
            return "SIN PROYECTOS ACTIVOS"


     
class WebsiteForm(WebsiteForm):

    def _handle_website_form(self, model_name, **kwargs):
        #model
        task_id = request.params.get('task_id')
        if task_id:
            task = request.env['project.task'].sudo().search([('id','=',task_id)])
            request.params['project_id'] = task[0].project_id.id
            del request.params['task_id']
            a = super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)
            alternative_a = json.loads(a)    
            modify_task = request.env['helpdesk.ticket'].sudo().search(   [('id','=',int(alternative_a['id']) )  ] )
            search_equip =""
            if task[0].project_id.name in ['Garantías Odoo']:
                    search_equip = "Garantías"
            elif task[0].project_id.name in ['Pólizas Odoo']:
                    search_equip = "Pólizas"        
            else:
                search_equip = "Proyecto en proceso"
            id_equip = request.env['helpdesk.team'].sudo().search(   [('name','=',search_equip)  ] ).id
            modify_task.sudo().write( {'task_id':task.id,'team_id':id_equip , 'project_id':task[0].project_id.id} )         
            return a
        a = super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)
       
        return a 