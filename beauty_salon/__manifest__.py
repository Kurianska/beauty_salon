{
    'name': 'Beauty Salon',
    'version': '15.0.1.0.0',
    'category': 'Services',
    'summary': 'Beauty Salon Management',
    'license': "LGPL-3",
    'author': "Uliana Kurianska",
    'website: https://beauty-salon.com'
    'description': """Manage beauty salon operations""",

    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/client_view.xml',
        'views/employee_view.xml',
        'views/visit_view.xml',
        'views/employee_schedule.xml',
        'report/model_report.xml',
        'report/report_employee_schedule_template.xml',
        'wizard/reschedule_visit_wizard.xml',
        'wizard/client_visit_reschedule_wizard.xml',
    ],
    'demo': [
        'demo/demo_employee.xml',
        'demo/demo_client.xml',
        'demo/demo_employee_schedule.xml',
        'demo/demo_visit.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
