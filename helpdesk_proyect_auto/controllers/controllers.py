
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
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.osv import expression
_logger = logging.getLogger(__name__)
import base64
from odoo.tools import ImageProcess
import werkzeug

class WebsiteTicketValidation(http.Controller):
    @http.route(['/mesa-de-ayuda'], type='http', auth="user", website=True)
    def create_icket(self, **kw):
        id_user = request.env.user.id
        user = request.env['res.users'].browse(id_user).partner_id
        for t  in request.env['sale.order.line'].search( [ ('order_id.partner_id','=',user.id),('order_id.partner_id.is_company','=',True) ] ): 
            values={}
            return request.render('website.mesa-de-ayuda', values)
        
        return request.render('website.mesa-de-ayuda')
        #"""This route is called when adding a product to cart (no options)."""
        #sale_order = request.website.sale_get_order(force_create=True)
        #if sale_order.state != 'draft':
        #    request.session['sale_order_id'] = None
        #    sale_order = request.website.sale_get_order(force_create=True)
       


        
# from odoo import http


# class Test(http.Controller):
#     @http.route('/test/test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test/test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test.listing', {
#             'root': '/test/test',
#             'objects': http.request.env['test.test'].search([]),
#         })

#     @http.route('/test/test/objects/<model("test.test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test.object', {
#             'object': obj
#         })
