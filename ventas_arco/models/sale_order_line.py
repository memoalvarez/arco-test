# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
   _inherit = 'sale.order.line'

   valorDeclarado = fields.Float(string="Valor Declarado")
   numeroDeBultos = fields.Float(string="N° Bultos")


   @api.model
   def create(self, vals):
      result = super(SaleOrderLine, self).create(vals)
      if result.product_id.barcode == 'ENVIO':
         producto = self.sudo().env['product.product'].search([('barcode', '=', 'SEGURO')])
         linea = {
            'order_id' : result.order_id.id,
            'product_id' : producto.id,
            'price_unit' : (result.valorDeclarado*8)/1000,
            'sequence' : 13
         }
         movimiento = self.env['sale.order.line'].create(linea)

      return result


   def write(self, vals):
      res = super(SaleOrderLine, self).write(vals)

      if 'valorDeclarado' in vals:
         if self.product_id.barcode == 'EC':
            producto = self.sudo().env['product.product'].search([('barcode', '=', 'SEGURO')])
            linea = {
               'order_id' : self.order_id.id,
               'product_id' : producto.id,
               'price_unit' : (vals.get('valorDeclarado')*8)/1000,
               'sequence' : 25
            }
            movimiento = self.env['sale.order.line'].create(linea)
         elif self.product_id.barcode == 'ENVIO':
            producto = self.sudo().env['product.product'].search([('barcode', '=', 'SEGURO')])
            linea = {
               'order_id' : self.order_id.id,
               'product_id' : producto.id,
               'price_unit' : (vals.get('valorDeclarado')*8)/1000,
               'sequence' : 12
            }
            movimiento = self.env['sale.order.line'].create(linea)

      return res


   
