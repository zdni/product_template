from odoo.tests.common import Form, TransactionCase
from odoo.tests import tagged
from odoo.exceptions import UserError, ValidationError


@tagged('post_install', '-at_install')
class TestProductMaterial(TransactionCase):
    def test_create_material(self):
        ''' Ensure you can't create material with buy price smaller than 100 '''

        supplier = self.env['res.partner'].create({
            'name': 'Your Supplier',
            'email': 'supplier@other.company.com',
            'supplier_rank': 10,
        })

        material_vals = {
            'name': 'Testing Material',
            'code': 'TM01',
            'type': 'fabric',
            'buy_price': 99.0,
            'supplier_id': supplier.id
        }

        self.assertLess(material_vals, 100.0, "Buy Price can't be set smaller than 100!")

        material_vals['buy_price'] = 100.0
        self.assertRaises(UserError, self.env['product.material'].create, material_vals)
        
        material = self.env['product.material'].create(material_vals)

        with self.assertRaises(UserError):
            material.buy_price = 99.0