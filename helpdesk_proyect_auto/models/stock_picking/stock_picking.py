# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime,date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from collections import defaultdict
class Stock_Picking(models.Model):
    _inherit  = "stock.move"
          
    def product_price_update_before_done(self, forced_qty=None):
        super(Stock_Picking, self).product_price_update_before_done( forced_qty=None)
        _logger.info(self.filtered(lambda move: move._is_in() and move.with_context(force_company=move.company_id.id).product_id.cost_method not in ('average', 'fifo') ))
        for move in self.filtered(lambda move: move._is_in() and move.with_context(force_company=move.company_id.id).product_id.cost_method not in ('average', 'fifo') ) :
              move.product_id.with_context(force_company=move.company_id.id).sudo().write({'standard_price': move._get_price_unit()})
              _logger.info("yeeeeeeeeeeeeeeeeeees")
    