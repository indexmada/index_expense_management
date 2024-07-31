# -*- coding: utf-8 -*-

{
    'name': 'Expense Management',
    'version': '1.0',
    'author': 'zoubli153',
    'category': 'POS',
    'website': '',
    'depends': ['point_of_sale'],
    'license': "AGPL-3",
    'data': [
            'security/ir.model.access.csv',
            'views/expense_management_views.xml',
            'wizard/expense_manag_views_wiz.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
    'icon': '/index_expense_management/static/description/icon.png',
}
