# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
   _inherit = 'account.move'

   aseguradora = fields.Char(string="Aseguradora", related='partner_id.aseguradora')
   noDePoliza = fields.Char(string="N° de póliza", related='partner_id.noDePoliza')
   
   paymentTerm = fields.Selection([('FP', 'Fletes pagados'), ('FC', 'Fletes por cobrar'), ('FR','Fletes C. Reg.')], string='Condiciones de pago')
   ruta = fields.Many2many('crm.tag', string="Ruta", related="stock_move_id.picking_id.ruta.id")
   
   @api.model
   def create(self, vals):
      result = super(AccountMove, self).create(vals)

      if result.partner_id.l10n_mx_edi_payment_method_id:
         result.l10n_mx_edi_payment_method_id = result.partner_id.l10n_mx_edi_payment_method_id.id

      if result.partner_id.l10n_mx_edi_usage:
         result.l10n_mx_edi_usage = result.partner_id.l10n_mx_edi_usage

      return result