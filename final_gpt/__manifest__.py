{
    'name': 'ChatGPT Integration',
    'version': '16.0.1.0.0',
    'summary': 'Integrate ChatGPT with Odoo',
    'description': 'A module to interact with ChatGPT, including custom styling and view integration.',
    'category': 'Tools',
    'author': 'Bofree',
    'website': 'http://www.example.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/chatgpt_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'FINAL_GPT\static\src\css\custom_styles.css',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
}
