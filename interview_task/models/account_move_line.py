from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    serial_ids = fields.Many2many(
        'stock.lot',
        string='Serial / Lot Numbers',
        domain="[('product_id', '=', product_id)]"
    )

    tracking = fields.Selection(
        related='product_id.tracking',
        readonly=True,
        string='Tracking'
    )
