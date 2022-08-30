# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProjectTaskType(models.Model):
   _inherit = 'project.task.type'

   project_task_function = fields.Selection([
        ('recepcion_nc', 'Recepcion no consolidado'),
        ('envio_nc', 'Envio no consolidado'),
        ('recepcion_c', 'recepcion consolidado'),
        ('envio_c', 'envio consolidado'),
        ('generar_cotizacion', 'Generar cotizacion'),
        ], string='Funcion de etapa')


   




