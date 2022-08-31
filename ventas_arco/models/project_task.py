# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _
import logging

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
   _inherit = 'project.task'

   almacen = fields.Many2one('stock.warehouse', "Almacen")
   guia_id = fields.Many2one('stock.picking', string="Informe")
   chofer = fields.Many2one('res.partner', string="Operador")
   unidad = fields.Many2one('unidades.unidades', string="Unidad")
   recoleccion = fields.Many2one('res.partner', string='Recolección')


   project_task_function = fields.Selection([
        ('recepcion_nc', 'Recepcion no consolidado'),
        ('envio_nc', 'Envio no consolidado'),
        ('recepcion_c', 'recepcion consolidado'),
        ('envio_c', 'envio consolidado'),
        ('generar_cotizacion', 'Generar cotizacion'),
        ], string='Funcion de etapa', related='stage_id.project_task_function')


   @api.model
   def create(self, vals):
      result = super(ProjectTask, self).create(vals)
      recoleccion = self.sudo().env['sale.order.line'].search([('order_id', '=', result.sale_line_id.order_id.id),('product_id.default_code', '=', 'RECOLECCION')])
      if len(recoleccion) > 0:
         etiqueta = self.sudo().env['project.tags'].search([('name', '=', 'RECOLECCION')])
         result.tag_ids = [(4, etiqueta.id)]
      
      return result



   def action_create_reception(self):
      if not self.almacen:
        raise ValidationError(_('Necesita seleccionar un almacén antes de crear recepción'))

      producto = self.sudo().env['product.product'].search([('default_code', '=', 'product')])

      vals = {
         'picking_type_id' : self.almacen.in_type_id.id,
         'location_dest_id' : self.almacen.in_type_id.default_location_dest_id.id,
         'location_id' : self.almacen.in_type_id.default_location_src_id.id,
         'project_task_id' : self.id,
         'destinatario' : self.partner_id.id
      }
      recepcion = self.env['stock.picking'].create(vals)

      linea = {
         'picking_id' : recepcion.id,
         'product_id' : producto.id,
         'name' : self.description,
         'location_id': self.almacen.in_type_id.default_location_src_id.id,
         'location_dest_id': self.almacen.in_type_id.default_location_dest_id.id,
         'description_picking' : self.description,
         'product_uom_qty' : self.sale_line_id.numeroDeBultos,
         'product_uom' : self.sale_line_id.product_uom.id,
         'project_task_id' : self.id
      }
      movimiento = self.env['stock.move'].create(linea)

   #Funcion para agrear productos de recepcion a guia (Informe)
   def action_add_to_guia(self):
      producto = self.sudo().env['product.product'].search([('default_code', '=', 'product')])
      bultos = 0
      ec_descripcion = ''
      peso = 0
      for record in self.reception_ids:
         if record.state == 'done':
            for line in record.move_ids_without_package:
               bultos += line.quantity_done
               peso += line.peso
               ec_descripcion = ec_descripcion + str(line.description_picking) + "\n"

      linea_guia = {
         'picking_id' : self.guia_id.id,
         'product_id' : producto.id,
         'name' : self.guia_id.name,
         'location_id': self.guia_id.location_id.id,
         'location_dest_id': self.guia_id.location_dest_id.id,
         'description_picking' : ec_descripcion,
         'product_uom_qty' : bultos,
         'product_uom' : producto.uom_id.id,
         'peso' : peso,
         'sale_line_id' : self.sale_line_id.id
      }
      movimiento = self.env['stock.move'].create(linea_guia)



   def action_view_guias(self):
      self.ensure_one()
      return {
         "type": "ir.actions.act_window",
         "res_model": "stock.picking",
         "views": [[False, "form"]],
         "res_id": self.guia_id.id,
         "context": {"create": False},
        }


   def action_create_reception_2(self):
      if not self.almacen:
        raise ValidationError(_('Necesita seleccionar un almacén antes de crear recepción'))
      action = self.env.ref('stock.stock_picking_action_picking_type').read()[0]
      action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
      action['context'] = {'default_picking_type_id': self.almacen.in_type_id.id, 'default_project_task_id' : self.id }
      action['target'] = 'new'

      return action
   
   def _compute_receptions_ids(self):
        for reg in self:
            receptions_count = reg.env['stock.picking'].search_count([('project_task_id', '=', reg.id)])
            reg.update({
                'reception_count': receptions_count,
            })
   
   reception_count = fields.Integer(string='Receptions count', compute='_compute_receptions_ids')
   reception_ids = fields.One2many('stock.picking', 'project_task_id', string='Recepciones')


   def action_view_receptions_2(self):
      self.ensure_one()
      recepciones = self.mapped('reception_ids')

      if len(recepciones) > 1:
            action = self.env.ref('stock.stock_picking_action_picking_type').read()[0]
            action['domain'] = [('id', 'in', recepciones.ids)]
            action['context'] = dict(create=False)
            return action

      elif recepciones:
            return {
               "type": "ir.actions.act_window",
               "res_model": "stock.picking",
               "views": [[False, "form"]],
               "res_id": recepciones.id,
               "context": {"create": False},
            }
   
   #Creacion de cotizacion desde tarea
   def action_create_cotizacion(self):
      producto = self.sudo().env['product.product'].search([('default_code', '=', 'EC')])
      plantilla = self.sudo().env['sale.order.template'].search([('name', '=', 'Envío')])

      bultos = 0
      ec_descripcion = ''

      for record in self.reception_ids:
         if record.state == 'done':
            for line in record.move_ids_without_package:
               bultos += line.quantity_done
               ec_descripcion = ec_descripcion + str(line.description_picking) + "\n"

      #Se crea diccionario para caratula de cotizacion
      vals = {
         'partner_id' : self.partner_id.id,
         'sale_order_template_id': plantilla.id
      }

      #Se crea corizacion y se agrega id a tarea
      sale_order = self.env['sale.order'].create(vals)
      self.sale_order_id = sale_order.id

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

      self.sale_line_id = linea.id


   def action_view_cotizaciones(self):
      self.ensure_one()
      return {
         "type": "ir.actions.act_window",
         "res_model": "sale.order",
         "views": [[False, "form"]],
         "res_id": self.sale_order_id.id,
         "context": {"create": False},
        }


   def action_add_to_report_view(self):
      return {
         'name': _('Agregar a informe'),
         'res_model': 'stock.picking.report',
         'view_mode': 'form',
         'context': {
               'active_model': 'project.task',
               'active_ids': self.ids,
         },
         'target': 'new',
         'type': 'ir.actions.act_window',
      }
