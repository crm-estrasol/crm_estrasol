from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PacklifeSaleOrder(models.Model):
    _inherit = 'sale.order'

    enable_collection = fields.Boolean('Habilitar Cobranza',copy=False)
    approve_sale = fields.Boolean('Aprobar',copy=False)
    id_user = fields.Integer(string='ID partner',related='partner_id.id')
    credit = fields.Float('Crédito',related='partner_id.credit_limit')
    
    
    """partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address',
        readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', partner_id)]",)
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address', readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=',partner_id)]",)
    """

    def enable_collection_change(self):
        self.enable_collection = True
    
    def approve_sale_function(self):
        self.approve_sale = True

    def action_cancel(self):
        self.enable_collection = False
        self.approve_sale = False
        return self.write({'state': 'cancel'})

class MailTemplate(models.Model):
    _inherit = "mail.template"

    def generate_email(self, res_ids, fields=None):
        self.ensure_one()
        res = super(MailTemplate, self).generate_email(res_ids, fields=fields)
        new_attachments = []
        
        for inv in res.keys():
          new_attachments = []
          model = res[ inv ]['model']
          i_r = res[ inv ]['res_id']  
          if model in ['account.move']:
            invoice = self.env[model].browse(i_r)
            if invoice.addenda_verify == 'SANMINA ADDENDA':
                for a in  res[ inv ]['attachments'] :
                    index = a[0].index('.')
                    value =   "%s_%s%s" % ( invoice.rfc_samina, invoice.pon_number,a[0][index:] )
                    new_attachments.append( ( value, a[1] ) )
                    res[ inv ]['attachments']  = new_attachments
            #_logger.info(self.env[self.model].browse(res_ids))
        #_logger.info( res[ list(res.keys())[0] ]['model']  )
        #_logger.info( res[ list(res.keys())[0] ]['res_id']  )
        #_logger.info(self.env[self.model].browse(res_ids))
        return res





    