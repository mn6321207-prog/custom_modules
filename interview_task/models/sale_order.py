from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    serial_ids = fields.Many2many('stock.lot', string='Serials')

    def _prepare_stock_moves(self, picking):
        res = super(SaleOrderLine, self)._prepare_stock_moves(picking)
        for re in res:
            re['lot_ids'] = [(6, 0, self.lot_ids.ids)]
        return res