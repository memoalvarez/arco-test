# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPickingReport(models.TransientModel):
   _name = 'stock.picking.report'
   _description = 'Informe'

   picking_id = fields.Many2one('stock.picking', string="Informe")

   def add_to_report_button(self):
      self.ensure_one()
      tareas = self.env['project.task'].browse(self._context.get('active_ids', []))

      for reg in tareas:
         reg.guia_id = self.picking_id.id
         reg.action_add_to_guia()
         
      return {
         "type": "ir.actions.act_window",
         "res_model": "stock.picking",
         "views": [[False, "form"]],
         "res_id": self.picking_id.id,
         "context": {"create": False},
      }

   def create_report_button(self):
      self.ensure_one()
   
      tipo_operacion = self.sudo().env['stock.picking.type'].search([('name', '=', 'Informes')])
      vals = {
         'picking_type_id' : tipo_operacion.id,
         'location_dest_id' : tipo_operacion.default_location_dest_id.id,
         'location_id' : tipo_operacion.default_location_src_id.id,
      }
      guia = self.env['stock.picking'].create(vals)
      tareas = self.env['project.task'].browse(self._context.get('active_ids', []))

      for reg in tareas:
         reg.guia_id = guia.id
         reg.action_add_to_guia()
         
      return {
         "type": "ir.actions.act_window",
         "res_model": "stock.picking",
         "views": [[False, "form"]],
         "res_id": guia.id,
         "context": {"create": False},
      }

