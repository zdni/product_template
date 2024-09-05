from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ProductMaterial(models.Model):
    _name = 'product.material'

    code = fields.Char('Material Code', required=True)
    name = fields.Char('Material Name', required=True)
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton'),
    ], string='Material Type', required=True, default='fabric')
    buy_price = fields.Float('Buy Price', required=True, default=100)
    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True)

    @api.onchange('buy_price')
    def _onchange_buy_price(self):
        if self.buy_price < 100:
            raise UserError(_("Buy Price can't be set smaller than 100!"))

    @api.model
    def create(self, vals):
        if 'buy_price' in vals and vals['buy_price'] < 100:
            raise UserError(_("Buy Price can't be set smaller than 100!"))

        return super(ProductMaterial, self).create(vals)