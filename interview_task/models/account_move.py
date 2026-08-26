from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    check = fields.Boolean(string='Check')
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    delivery_id = fields.Many2one('stock.picking', string='Delivery Order')
    delivery_count = fields.Integer(string='Delivery Order Count')

    # @api.model
    def action_post(self):
        res = super().action_post()
        if self.check == False:
            for line in self.invoice_line_ids:
                if line.product_id.type == 'consu':
                    if line.quantity > line.product_id.qty_available:
                        raise UserError(
                            f'The available  "{line.product_id.name}"  is lower than the required quantity by '
                            f'{line.quantity - line.product_id.qty_available} units.'
                        )
            vals = {
                'partner_id': self.partner_id.id,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.price_unit,
                    'name': line.name,
                    'serial_ids': line.serial_ids.ids,
                }) for line in self.invoice_line_ids],

            }
            print(vals)
            sale = self.env['sale.order'].create(vals)

            self.check = True

            sale.action_confirm()
            for invoice_line, sale_line in zip(self.invoice_line_ids, sale.order_line):
                invoice_line.sale_line_ids = [(4, sale_line.id)]
            self.delivery_count = sale.delivery_count


            if sale.picking_ids:

                for stock in sale.picking_ids:
                    self.delivery_id = stock.id
                    stock.button_validate()
                    stock.button_validate()

        return res





    def action_delivery_related(self):
        action = self.env['ir.actions.actions']._for_xml_id('stock.action_picking_tree_all')
        view_id = self.env.ref('stock.view_picking_form').id
        action['res_id'] = self.delivery_id.id
        action['views'] = [[view_id, 'form']]
        return action