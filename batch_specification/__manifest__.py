# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Batch Specification',
    'version': '13.0.1.0',
    'category': 'Product',
    'website': 'www.caretit.com',
    'author': 'Caret IT Solutions Pvt. Ltd',
    'images': [],
    'depends': ['product','stock','mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/mrp_production.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
