# -*- coding: utf-8 -*-

from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def do_quantity_done(self):
        for lot in self:
            lot.write({'qty_done': lot.qty_done + lot.product_uom_qty})
            lot.move_id.write({'quantity_done': sum(move_id.qty_done
                for move_id in lot.move_id.move_line_ids)})
            return self.mapped('move_id').action_show_details()

