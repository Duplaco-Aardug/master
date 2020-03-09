# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################


{
    'name' : 'Copmany On Lot',
    'version' : '0.1',
    'category': 'Production',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'description' : """
        company field on lot without multi company option.
    """,
    'depends': ['base', 'stock'],
    'data': [
        'views/lot_view.xml',
    ],
}
