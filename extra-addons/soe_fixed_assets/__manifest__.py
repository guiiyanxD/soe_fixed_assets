# -*- coding: utf-8 -*-

{
    'name': "soe_fixed_assets",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'report/tech_report_requests/technical_report_request_report.xml',
        'report/tech_report_requests/technical_report_request_template.xml',
        'report/loans/asset_loans_report.xml',
        'report/loans/asset_loans_template.xml',
        'report/technical_details/technical_request_details_report.xml',
        'report/technical_details/technical_request_details_template.xml',
        'report/tech_report_to_unavailable/tech_report_to_unavailable_report.xml',
        'report/tech_report_to_unavailable/tech_report_to_unavailable_template.xml',
        'report/tech_report_to_maintenance/tech_report_to_maintenance_report.xml',
        'report/tech_report_to_maintenance/tech_report_to_maintenance_template.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/asset_views.xml',
        'views/area_views.xml',
        'views/physical_status_views.xml',
        'views/group_views.xml',
        'views/measure_views.xml',
        'views/ubications_views.xml',
        'views/aaset_loans_views.xml',
        'views/acquisition_views.xml',
        'views/acquisition_detail_views.xml',
        'views/technical_report_request_views.xml',
        'views/technical_report_request_detail_views.xml',
        'views/technical_report_request_detail_status_views.xml',
        'data/daily_check_expired_loans_cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets':{
        'web.assets_backend':[
            # 'soe_fixed_assets/static/src/js/fecha_validacion.js',
        ]
    }
}



