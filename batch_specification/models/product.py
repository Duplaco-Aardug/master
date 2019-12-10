# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError

class ProductFieldConfig(models.Model):

    _name = 'product.field.config'
    _description = 'Product Field Configuration'

    name = fields.Char(string='Name')
    maximum = fields.Char(string='Maximum')
    minimum = fields.Char(string="Minimum")
    check_required = fields.Boolean(string="Required")
    product_id = fields.Many2one('product.template')

    @api.model
    def create(self,vals):
        if vals['check_required']:
            if not vals['maximum'] or not vals['minimum']:
                raise UserError(_('Please fill all fields.'))
            else:
                return super(ProductFieldConfig,self).create(vals)
        else:
            return super(ProductFieldConfig,self).create(vals)

    def write(self,vals):
        flag = 0
        # checked this condition when required field value change.
        if 'check_required' in vals:
            if vals['check_required']:
                if 'maximum' in vals:
                    if not vals['maximum']:
                        flag = 1
                elif not self.maximum:
                    flag = 1
                if 'minimum' in vals:
                    if not vals['minimum']:
                        flag = 1
                elif not self.minimum:
                    flag = 1
        # checked this condition when maximum or minimum field's value change.
        elif self.check_required:
            if 'maximum' in vals:
                if not vals['maximum']:
                    flag = 1
            if 'minimum' in vals:
                if not vals['minimum']:
                    flag = 1
        if flag:
            raise UserError(_('Please fill all fields'))
        else:
            return super(ProductFieldConfig,self).write(vals)

class ProductTemplate(models.Model):

    _inherit = 'product.template'

    product_field_ids = fields.Many2many('product.field.config',
    string='Product Fields')

    @api.model
    def create(self,vals):
        res = super(ProductTemplate,self).create(vals)
        config_field_ids = self.env['product.field.config'].search([
            ('check_required','=',True)])
        res.product_field_ids = config_field_ids.ids
        return res

class ProductField(models.Model):
    _name = 'product.field'
    _description = 'Product Field'

    name = fields.Char(string='Name',readonly=True)
    maximum = fields.Char(string='Maximum', readonly=True)
    minimum = fields.Char(string="Minimum", readonly=True)
    actual_value = fields.Char(string='Actual Value')

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_field_ids = fields.Many2many('product.field',
        string='Product Fields')

    @api.model
    def create(self, vals):
        product= self.env['product.product'].browse(vals.get('product_id'))
        vals.update({'product_field_ids':[(0,0,{'name':line.name,
            'maximum':line.maximum, 'minimum':line.minimum})
        for line in product.product_field_ids]})
        return super(ProductionLot, self).create(vals)


    def write(self, vals):
        res=super(ProductionLot, self).write(vals)
        if 'product_id' in vals.keys():
            product= self.env['product.product'].browse(vals.get('product_id'))
            self.write({'product_field_ids':[(0,0,{'name':line.name,
                'maximum':line.maximum, 'minimum':line.minimum})
            for line in product.product_field_ids]})
        return res
  
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_field_ids =[]

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    lots_ids = fields.Many2many('stock.production.lot',
        compute='_compute_lots_ids', string='Lots')
    _count_lots = fields.Integer(string='Lots count',
        compute='_compute_lots_ids')


    @api.depends('state')
    def _compute_lots_ids(self):
        for rec in self:
            lot = []
            for move_ids in rec.move_raw_ids:
                for move_lot_id in move_ids.move_line_ids:
                    for lot_id in move_lot_id.lot_id:
                        lot.append(lot_id.id)
            for move_finish_id in rec.move_finished_ids:
                for move_finish_lot_id in move_finish_id.move_line_ids:
                    for finish_lot_id in move_finish_lot_id.lot_id:
                        lot.append(finish_lot_id.id)
            rec._count_lots = len(lot)
            rec.lots_ids = lot


    def action_view_lots(self):
        action = self.env.ref('stock.action_production_lot_form')
        result = action.read()[0]
        result['context'] = {}
        lot_ids = sum([order.lots_ids.ids for order in self], [])
        if len(lot_ids) > 0:
            result['domain'] = "[('id','in',[" + ','.join(map(str, lot_ids)) + "])]"
        return result


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lot_ids = fields.Many2many('stock.production.lot',
        compute='_compute_lot_ids', string='Lots')
    _count = fields.Integer(string='Lots count', compute='_compute_lot_ids')


    @api.depends('state')
    def _compute_lot_ids(self):
        lot = []
        for pack_ids in self.move_line_ids:
            for pack_lot_id in pack_ids.lot_id:
                lot.append(pack_lot_id.id)
        self._count = len(lot)
        self.lot_ids = lot


    def action_view_lot(self):
        action = self.env.ref('stock.action_production_lot_form')
        result = action.read()[0]
        result['context'] = {}
        lots_ids = sum([order.lot_ids.ids for order in self], [])
        if len(lots_ids) > 0:
            result['domain'] = "[('id','in',[" + ','.join(map(str, lots_ids)) + "])]" 
        return result