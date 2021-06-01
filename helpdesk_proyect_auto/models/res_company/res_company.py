# -*- coding: utf-8 -*-

import datetime
from lxml import etree
from dateutil.relativedelta import relativedelta
import re
import logging
from pytz import timezone

import requests

from odoo import api, fields, models
from odoo.addons.web.controllers.main import xml2json_from_elementtree
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

BANXICO_DATE_FORMAT = '%d/%m/%Y'

_logger = logging.getLogger(__name__)

class ResCompanyTomcat(models.Model):
    _inherit = 'res.company'
    #Change to FIX
    #Override
    def _parse_banxico_data(self, available_currencies):
        """Parse function for Banxico provider.
        * With basement in legal topics in Mexico the rate must be **one** per day and it is equal to the rate known the
        day immediate before the rate is gotten, it means the rate for 02/Feb is the one at 31/jan.
        * The base currency is always MXN but with the inverse 1/rate.
        * The official institution is Banxico.
        * The webservice returns the following currency rates:
            - SF46410 EUR
            - SF60632 CAD
            - SF43718 USD Fixed
            - SF46407 GBP
            - SF46406 JPY
            - SF60653 USD SAT - Officially used from SAT institution
        Source: http://www.banxico.org.mx/portal-mercado-cambiario/
        """
        icp = self.env['ir.config_parameter'].sudo()
        token = icp.get_param('banxico_token')
        if not token:
            # https://www.banxico.org.mx/SieAPIRest/service/v1/token
            token = 'd03cdee20272f1edc5009a79375f1d942d94acac8348a33245c866831019fef4'  # noqa
            icp.set_param('banxico_token', token)
        foreigns = {
            # position order of the rates from webservices
            'SF46410': 'EUR',
            'SF60632': 'CAD',
            'SF46406': 'JPY',
            'SF46407': 'GBP',
            #CHANGED THIS TO FIX
            'SF43718': 'USD',
        }
        url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/%s/datos/%s/%s?token=%s' # noqa
        try:
            date_mx = datetime.datetime.now(timezone('America/Mexico_City'))
            today = date_mx.strftime(DEFAULT_SERVER_DATE_FORMAT)
            yesterday = (date_mx - datetime.timedelta(days= 3 if date_mx.weekday() == 0 else 1  )).strftime(DEFAULT_SERVER_DATE_FORMAT)
            res = requests.get(url % (','.join(foreigns), yesterday, today, token))
            res.raise_for_status()
            
            series = res.json()['bmx']['series']
          
            series = {serie['idSerie']: {dato['fecha']: dato['dato'] for dato in serie['datos']} for serie in series if 'datos' in serie}
            _logger.info(series)
            
        except:
            return False

        available_currency_names = available_currencies.mapped('name')

        rslt = {
            'MXN': (1.0, fields.Date.today().strftime(DEFAULT_SERVER_DATE_FORMAT)),
        }
     
        today = date_mx.strftime(BANXICO_DATE_FORMAT)
        yesterday = (date_mx - datetime.timedelta(days=1)).strftime(BANXICO_DATE_FORMAT)
        for index, currency in foreigns.items():
            if not series.get(index, False):
                return False
            if currency not in available_currency_names:
                continue

            serie = series[index]

            
            for rate in reversed(list(serie.keys())) :
                try:
                    foreign_mxn_rate = float(serie[rate])
                except (ValueError, TypeError):
                    return False
                foreign_rate_date = datetime.datetime.strptime(today, BANXICO_DATE_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
                rslt[currency] = (1.0/foreign_mxn_rate, foreign_rate_date)
                 
        return rslt