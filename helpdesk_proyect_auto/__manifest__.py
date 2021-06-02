# -*- coding: utf-8 -*-
{
    'name': "PackLife",

    'summary': """
        New features Odoo""",

    'description': """
        Inherit some views , new vies , reports
    """,

    'author': "Estrasol -Kevin Daniel del Campo",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','sale','sale_timesheet','sale_project', 'hr_timesheet','project','website_form'],

    # always loadedd
    'data': [
        'views/project/project.xml',
       'data/status_project.xml',
       'views/project/ticket_portal.xml',
        
    ],  
    'qweb': [
          #'qweb/replace_menu_base.xml',
        ]
        ,
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
}
