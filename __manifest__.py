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
            'views/expense_journal_view.xml',
            'views/expense_management_views.xml',
            'views/inherit_pos_config_view.xml',
            'views/inherit_pos_session_view.xml',
            'wizard/expense_manag_views_wiz.xml',
            'wizard/expense_detail_wizard.xml',
            'wizard/inherit_cash_box_out_wizard.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
    'icon': '/index_expense_management/static/description/icon.png',
}
