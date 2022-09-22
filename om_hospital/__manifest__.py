{
    'depends': [
        'sale',
        'mail',
        'website_slides',
        'hr',
    ],
    'name': 'hospital',
    'data': [
        'views/patient.xml',
        'views/sale.xml',
        'data/data.xml',
        'views/kids_views.xml',
        'views/patient_gender_views.xml',
        'wizard/create_appointment_views.xml',
        'wizard/search_appointment_views.xml',
        'views/appointment_views.xml',
        'views/doctor_views.xml',
        'report/report.xml',
        'report/patient_card.xml',
        'security/ir.model.access.csv'
    ]
}