    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _

class packlifeAccountMove(models.Model):
    _inherit  = 'account.move'
    """
    @api.model
    def _default_opening_balance(self):
        #Search last bank statement and set current opening balance as closing balance of previous one
        journal_id = self._context.get('default_journal_id', False) or self._context.get('journal_id', False)
        if journal_id:
            return self._get_opening_balance(journal_id)
        return 0
    """
    x_warehouse_especial = fields.Many2one(related='invoice_user_id.x_warehouse_especial')
    addenda_verify = fields.Char(related="partner_id.l10n_mx_edi_addenda.name")
    pon_number = fields.Char(string="PONumber",default="No aplica")
    email_samina = fields.Char(default=lambda self: self.env.company.email,string="Email compañia" )
    name_samina = fields.Char(default=lambda self: self.partner_id.name,string="Razon social completa Sanmina" )
    rfc_samina = fields.Char(default=lambda self: self.partner_id.vat, string="RFC" )
    supplier_samina = fields.Char(default="PROVEEDOR" ,string="Numero proveedor asignado")
    
    @api.onchange('partner_id')
    def _on_change_adenda(self):  
        if self.addenda_verify == 'SANMINA ADDENDA':  
            self.name_samina = self.partner_id.name
            self.rfc_samina = self.partner_id.vat
    def _get_currency_rate(self):
        currency_rate = self.env['res.currency']._get_conversion_rate(self.company_id.currency_id, self.currency_id, self.company_id, self.date)
        return  '{0:,.4f}'.format( 1/currency_rate )