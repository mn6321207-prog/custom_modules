from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_confirm(self, merge=True, merge_into=False, create_proc=True, **kwargs):
        moves = super()._action_confirm(merge=merge, merge_into=merge_into, create_proc=create_proc, **kwargs)
        for move in moves:
            if move.sale_line_id and move.sale_line_id.serial_ids and not move.lot_ids:
                move.lot_ids = move.sale_line_id.serial_ids
        return moves


