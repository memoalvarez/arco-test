# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
   _inherit = 'stock.move'

   sale_line_id = fields.Many2one('sale.order.line', string="Linea de pedido de venta")
   project_task_id = fields.Many2one('project.task', string="Tarea")
   descripcion2 = fields.Char('Descripcion')
   peso = fields.Float(string="Peso (Kg)")
   sOrganizacion = fields.Float('S Organización', compute="_compute_valor_envio")
   valorDeclarado = fields.Float('Valor declarado', compute="_compute_valor_envio")
   seguro = fields.Float('Seguro', compute="_compute_valor_envio")
   maniobras = fields.Float('Maniobras', compute="_compute_valor_envio")
   entregaDomicilio = fields.Float('Entrega a domicilio', compute="_compute_valor_envio")
   recoleccion = fields.Float('Recolección', compute="_compute_valor_envio")
   iva = fields.Float('IVA', compute="_compute_valor_envio")
   valortotalSorganizacion = fields.Float(string="$", compute="_compute_valor_envio")
   valorTotalDeclarado = fields.Float(string="$", compute="_compute_valor_envio")
   valorTotalSeguro = fields.Float(string="$", compute="_compute_valor_envio")
   valorTotalManiobras = fields.Float(string="$", compute="_compute_valor_envio")
   valorTotalEntrega = fields.Float(string="$", compute="_compute_valor_envio")
   valorTotalRecoleccion = fields.Float(string="$", compute="_compute_valor_envio")
   ivaTotal = fields.Float('$', compute="_compute_valor_envio")
   total = fields.Float('$', compute="_compute_valor_envio")
   totalFinal = fields.Float('$', compute="_compute_valor_envio")
   facturaTotal = fields.Integer('FP', compute="_compute_valor_envio")
   comision = fields.Float('$', compute="_compute_valor_envio")
   subtotal = fields.Float('$', compute="_compute_valor_envio")
   ivaPerm = fields.Float('$', compute="_compute_valor_envio")
   totalperm = fields.Float('$', compute="_compute_valor_envio")
   fletesFc = fields.Integer('$', compute="_compute_valor_envio")
   fletesFcr = fields.Integer('$', compute="_compute_valor_envio")
   fletesFp = fields.Integer('$', compute="_compute_valor_envio")
   comisionSeguro = fields.Float('$', compute="_compute_valor_envio")
   subtotalSeguro = fields.Float('$', compute="_compute_valor_envio")
   ivaPermSeguro = fields.Float('$', compute="_compute_valor_envio")
   totalpermSeguro = fields.Float('$', compute="_compute_valor_envio")
   totalInfoSeguro = fields.Float('$', compute="_compute_valor_envio")
   ivaInfoSeguro = fields.Float('$', compute="_compute_valor_envio")


   @api.depends('sale_line_id')
   def _compute_valor_envio(self):
      total = 0
      total2 = 0
      total3 = 0
      total4 = 0
      total5 = 0
      total6 = 0
      ivaCalc = 0
      totalIva = 0
      totalFinal = 0
      facTotal = 0
      comision = 0
      fletesp = 0
      fletesfcr = 0
      fletesfp = 0
      totalseguro = 0
      totalmaniobras = 0
      totalIvaSeguro = 0
      totalFinalseguro = 0
      
      for line in self:
         linea = self.env['sale.order.line'].search([('product_id.barcode', '=', 'SEGURO'), ('order_id', '=', line.sale_line_id.order_id.id)])
         lineaManiobras = self.env['sale.order.line'].search([('product_id.barcode', '=', 'MANIOBRAS'), ('order_id', '=', line.sale_line_id.order_id.id)])
         lineaRecoleccion = self.env['sale.order.line'].search([('product_id.barcode', '=', 'RECOLECCION'), ('order_id', '=', line.sale_line_id.order_id.id)])
         lineaEntrega = self.env['sale.order.line'].search([('product_id.barcode', '=', 'ENTREGA'), ('order_id', '=', line.sale_line_id.order_id.id)])
         
         suma = line.sale_line_id.price_unit
         iva1 = suma * .16
         total = suma + total
         
         sumaValorDeclarado = line.sale_line_id.valorDeclarado
         iva2 = sumaValorDeclarado * .16
         total2 = sumaValorDeclarado + total2
         
         sumaSeguro = linea.price_unit
         iva3 = sumaSeguro * .16
         total3 = sumaSeguro + total3
         
         sumaManiobras = lineaManiobras.price_unit
         iva4 = sumaManiobras * .16
         total4 = sumaManiobras + total4
         
         sumaEntrega = lineaEntrega.price_unit
         iva5 = sumaEntrega * .16
         total5 = sumaEntrega + total5
         
         sumaRecoleccion = lineaRecoleccion.price_unit
         iva6 = sumaRecoleccion * .16
         total6 = sumaRecoleccion + total6
         
         ivaCalc = iva1 + iva2 + iva3 + iva4 + iva5 + iva6
         totalIva = ivaCalc + totalIva
         
         totalAll = suma + sumaValorDeclarado + sumaSeguro + sumaManiobras + sumaEntrega + sumaRecoleccion + ivaCalc
         totalFinal = totalAll + totalFinal
         
         if line.sale_line_id.order_id.invoice_ids.id:
            facTotal = facTotal + 1
   
         if line.sale_line_id.order_id.invoice_ids.paymentTerm == 'FP':
            fletesfp = fletesfp + 1
         elif line.sale_line_id.order_id.invoice_ids.paymentTerm == 'FC':
            fletesp = fletesp + 1
         elif line.sale_line_id.order_id.invoice_ids.paymentTerm == 'FR':
            fletesfcr = fletesfcr + 1
         
         comision = (total + total4) * .10
         subtotal = comision + total3
         ivaperm = subtotal * .16
         totalperm = subtotal + ivaperm
         
         comision2 = (total + (total4 * .50)) * .10
         subtotal2 = (total3 * .5) + comision2
         ivaperm2 = subtotal2 * .16
         totalperm2 = subtotal2 + ivaperm2
         
         sumaSeguro2 = linea.price_unit * .50
         totalseguro += sumaSeguro
         ivaseguro = sumaSeguro2 * .16
         
         sumaManiobras2 = lineaManiobras.price_unit * .50
         totalmaniobras += sumaManiobras2
         ivamaniobras = sumaManiobras * .16
         
         ivaCalcSeguro = iva1 + iva2 + ivaseguro + ivamaniobras + iva5 + iva6
         totalIvaSeguro = ivaCalcSeguro + totalIvaSeguro
         
         totalAllseguro = suma + sumaValorDeclarado + sumaSeguro2 + sumaManiobras2 + sumaEntrega + sumaRecoleccion + ivaCalcSeguro
         totalFinalseguro = totalAllseguro + totalFinalseguro
         
         
         line.update({
                'sOrganizacion': line.sale_line_id.price_unit,
                'valorDeclarado': line.sale_line_id.valorDeclarado,
                'seguro': linea.price_unit,
                'maniobras':lineaManiobras.price_unit,
                'recoleccion':lineaRecoleccion.price_unit,
                'entregaDomicilio':lineaEntrega.price_unit,
                'valortotalSorganizacion': total,
                'valorTotalDeclarado': total2,
                'valorTotalSeguro': total3,
                'valorTotalManiobras': total4,
                'valorTotalEntrega': total5,
                'valorTotalRecoleccion': total6,
                'iva': ivaCalc,
                'ivaTotal': totalIva,
                'total': totalAll,
                'totalFinal': totalFinal,
                'facturaTotal': facTotal,
                'comision': comision,
                'subtotal': subtotal,
                'ivaPerm': ivaperm,
                'totalperm': totalperm,
                'fletesFc': fletesp,
                'fletesFcr': fletesfcr,
                'fletesFp': fletesfp,
                'comisionSeguro': comision2,
                'subtotalSeguro': subtotal2,
                'ivaPermSeguro': ivaperm2,
                'totalpermSeguro': totalperm2,
                'ivaInfoSeguro': totalIvaSeguro,
                'totalInfoSeguro': totalFinalseguro,
            })
         
   @api.onchange('description_picking')
   def _onchange_description_picking(self):
      if self.descripcion2:
         self.description_picking = self.descripcion2