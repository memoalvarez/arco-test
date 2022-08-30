# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UnidadesUnidades(models.Model):
   _name = 'unidades.unidades'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Unidades Arco'


   name = fields.Char(string="Unidad")
   marca = fields.Char(strig="Marca")
   permisionario = fields.Many2one('res.partner', string="Permisionario")
   descripcion = fields.Html(string="Descripcion")
   placas = fields.Char(string='Placas')
   modelo = fields.Char(string="Modelo")
   llantas = fields.Integer(string="Llantas")
   operador = fields.Many2one('res.partner', string="Operador")
   serialNumber = fields.Char(string="Numero de serie")
   tarjetaCirculante = fields.Char(string="Tarjeta de circulacion")
   vencimientoPoliza = fields.Date(string="Vencimiento de póliza")


   def name_get(self):
      result = []
      for prod in self:
         result.append((prod.id, "%s - %s" % (prod.name, prod.placas or '')))
      return result

   


   


   




