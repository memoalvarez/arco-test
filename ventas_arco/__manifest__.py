# -*- coding: utf-8 -*-
{
    'name': "Ventas arco",

    'summary': """
        Ventas arco
        """,

    'description': """
        Ventas arco
    """,

    'author': "Assetel",
    'website': "http://www.assetel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'stock', 'contacts', 'account_accountant', 'l10n_mx_edi'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/informe_seguro.xml',
        'views/informe_viaje.xml',
        'views/project_task_type.xml',
        'views/project_task.xml',
        'views/sale_order.xml',
        'views/sale_report_inherit.xml',
        'views/stock_picking.xml',
        'views/stock_picking_menu.xml',
        'views/unidades_unidades_menu.xml',
        'views/unidades_unidades.xml',
        'views/res_partner.xml',
        'views/account_move.xml',
        'views/stock_picking_report.xml',
        'views/report_invoice.xml',
    ],
}