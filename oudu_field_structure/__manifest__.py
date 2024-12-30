# -*- coding: utf-8 -*-
{
    'name': "字段查看",
    'author': '永',
    'company': '2634800669@qq.com',
    'summary': "可以快速查找两个模型之间的关联字段",
    "version": "17.0.1.0.0",
    'sequence': 3,
    'description': """
    字段查看
    """,
    'version': '1.1',
    'depends': ['base'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/oudu_field_structure_view.xml',
    ],
    "license": "LGPL-3",
    # Author
    "installable": True,
    "application": False,
    "auto_install": False,
}
