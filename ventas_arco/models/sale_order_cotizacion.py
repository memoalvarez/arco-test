# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderCotizacion(models.TransientModel):
   _name = 'sale.order.cotizacion'
   _description = 'Orden de venta'

   cotizacion_id = fields.Many2one('sale.order', string="Orden de venta")

   def create_report_button(self):
      self.ensure_one()
      tareas = self.env['project.task'].browse(self._context.get('active_ids', []))
      producto = self.sudo().env['product.product'].search([('default_code', '=', 'EC')])
      plantilla = self.sudo().env['sale.order.template'].search([('name', '=', 'Envío')])
      
      bultos = 0
      ec_descripcion = ''

      #Se crea diccionario para caratula de cotizacion
      vals = {
         'partner_id' : tareas[0].id,
         'sale_order_template_id': plantilla.id
      }
      sale_order = self.env['sale.order'].create(vals)
      
      for tarea in tareas:
         tarea.sale_order_id = sale_order.id
         for record in tarea.reception_ids:
            if record.state == 'done':
               for line in record.move_ids_without_package:
                  bultos += line.quantity_done
                  ec_descripcion = ec_descripcion + str(line.description_picking) + "\n"
         
      seq = 10
      #Esto sirve para agregar las lineas de la plantilla a la orden
      for line in plantilla.sale_order_template_line_ids:
         vals = {
            'sequence' : seq,
            'order_id' : sale_order.id,
            'display_type': line.display_type,
            'name' : line.name
         }
         linea = self.env['sale.order.line'].create(vals)
         seq += 10
      
      vals = {
            'order_id' : sale_order.id,
            'sequence' : 15,
            'product_id' : producto.id,
            'name': ec_descripcion,
            'numeroDeBultos': bultos
      }
      linea = self.env['sale.order.line'].create(vals)
      
      for tarea in tareas:
         tarea.sale_line_id = linea.id

      return {
         "type": "ir.actions.act_window",
         "res_model": "sale.order",
         "views": [[False, "form"]],
         "res_id": self.cotizacion_id.id,
         "context": {"create": False},
      }


