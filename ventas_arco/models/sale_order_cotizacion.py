# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderCotizacion(models.TransientModel):
   _name = 'sale.order.cotizacion'
   _description = 'Orden de venta'

   cotizacion_id = fields.Many2one('sale.order', string="Orden de venta")

   def add_to_report_button(self):
      self.ensure_one()
      tareas = self.env['project.task'].browse(self._context.get('active_ids', []))

      for reg in tareas:
         reg.sale_order_id = self.cotizacion_id.id
         reg.action_create_cotizacion()
         
      return {
         "type": "ir.actions.act_window",
         "res_model": "sale.order",
         "views": [[False, "form"]],
         "res_id": self.cotizacion_id.id,
         "context": {"create": False},
      }

   def create_report_button(self):
      self.ensure_one()
   
      plantilla2 = self.sudo().env['sale.order.template'].search([('name', '=', 'Envío')])
      
      #Se crea diccionario para caratula de cotizacion
      vals = {
         'partner_id' : self.partner_id.id,
         'sale_order_template_id': plantilla2.id
      }
      #Se crea cotizacion y se agrega id a tarea
      sale_order = self.env['sale.order'].create(vals)
      
      tareas = self.env['project.task'].browse(self._context.get('active_ids', []))

      for reg in tareas:
         reg.sale_order_id = sale_order.id
         reg.action_create_cotizacion()
         
      return {
         "type": "ir.actions.act_window",
         "res_model": "sale.order",
         "views": [[False, "form"]],
         "res_id": sale_order.id,
         "context": {"create": False},
      }

