# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project_task_id = fields.Many2one('project.task')
    chofer = fields.Many2one('res.partner', string="Operador")
    ruta = fields.Many2many('crm.tag' ,string="Rutas")
    permisionario = fields.Many2one('res.partner', string="Permisionario")
    unidad = fields.Many2one('unidades.unidades', string="Unidad")
    sOrganizacion = fields.Float(string="S Organización", compute="_compute_valor_permisionario")
    totalMonto = fields.Float(string="Montos", compute="_compute_valor_permisionario")
    receivedBy = fields.Many2one('res.partner', string="Recibido por")
    tipodeoperacion2 = fields.Selection(related="picking_type_id.code", string="Tipo de operacion")
    
    sequence_code2 = fields.Char(related="picking_type_id.sequence_code", string="Código")
    destinatario = fields.Many2one('res.partner', string="Destinatario")

    @api.depends('move_ids_without_package')
    def _compute_valor_permisionario(self):
        for reg in self:
            total = 0
            total2 = 0
            for line in reg.move_ids_without_package:
                total += line.sOrganizacion
                total2 += line.total
                
            reg.update({
                'sOrganizacion': total,
                'totalMonto': total2,
            })


    def action_view_task(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "views": [[False, "form"]],
            "res_id": self.project_task_id.id,
            "context": {"create": False},
        }
        
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for line in self.move_ids_without_package:
            line.description_picking = line.descripcion2
