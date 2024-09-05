from odoo import http
from odoo.http import request, Response
from werkzeug.exceptions import BadRequest, InternalServerError
import json
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class ProductMaterial(http.Controller):

    @http.route('/product_materials', type='http', auth='user')
    def index(self, **post):
        try:
            headers = {'Content-Type': 'application/json'}

            search_value = post.get('search')
            domain = []
            if search_value:
                domain += [
                    '|',
                    ('name', 'ilike', search_value),
                    ('type', 'ilike', search_value),
                ]
            records = request.env['product.material'].sudo().search(domain)
            
            materials = []
            for rec in records:
                val = {
                    "id": rec.id,
                    "name": rec.name,
                    "code": rec.code,
                    "type": rec.type,
                    "buy_price": rec.buy_price,
                    "supplier_id": rec.supplier_id.id,
                }
                materials.append(val)

            data = json.dumps(materials)
            return Response(data, headers=headers)
        except Exception as e:
            return Response(json.dumps({
                "success": False,
                "error_message": f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            }), 400)

    @http.route('/product_materials/get/<int:rec_id>', type='http', auth='user')
    def show(self, rec_id):
        try:
            headers = {'Content-Type': 'application/json'}

            record = request.env['product.material'].sudo().search([['id', '=', rec_id]])
            if len(record) == 0:
                return Response(json.dumps({
                    "success": False,
                    "message": "ID not found"
                }), status=400)

            val = {
                "id": record.id,
                "name": record.name,
                "code": record.code,
                "type": record.type,
                "buy_price": record.buy_price,
                "supplier_id": record.supplier_id.id,
            }

            data = json.dumps(val)
            return Response(data, headers=headers)
        except:
            return Response(json.dumps({
                "success": False,
                "message": "Internal Server Error"
            }), 500)

    @http.route('/product_material/update', auth='user', method=['PUT'], csrf=False)
    def update(self, **params):
        try:
            headers = {'Content-Type': 'application/json'}
            data = json.loads(request.httprequest.data)

            code = data['code']
            name = data['name']
            type = data['type']
            buy_price = data['buy_price']
            supplier_id = data['supplier_id']
            rec_id = data['id']

            record = request.env['product.material'].sudo().search([['id', '=', rec_id]])
            if len(record) == 0:
                return Response(json.dumps({
                    "success": False,
                    "message": "ID not found"
                }), status=400)

            record.sudp().write({
                "name": record.name,
                "code": record.code,
                "type": record.type,
                "buy_price": record.buy_price,
                "supplier_id": record.supplier_id.id,
            })

            data = json.dumps({ 'success': True, 'message': 'Success Update Material!' })
            return Response(data, headers=headers)
        except:
            return Response(json.dumps({
                "success": False,
                "message": "Internal Server Error"
            }), 500)

    @http.route('/product_material/delete', type='http', auth='user', method=['DELETE'])
    def delete(self, **params):
        try:
            headers = {'Content-Type': 'application/json'}
            data = json.loads(request.httprequest.data)
            
            rec_id = data['id']

            record = request.env['product.material'].sudo().search([['id', '=', rec_id]])
            if len(record) == 0:
                return Response(json.dumps({
                    "success": False,
                    "message": "ID not found"
                }), status=400)
            
            record.unlink()

            data = json.dumps({ 'success': True, 'message': 'Success Delete Material!' })
            return Response(data, headers=headers)
        except:
            request.env.cr.rollback()
            return Response(json.dumps({
                "success": False,
                "message": "Internal Server Error"
            }), 500)