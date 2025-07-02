# from odoo import models, fields, api
#
#
# class JefaturaArea(models.Model):
#     _name = 'soe_fixed_assets.jefautra_area'
#     _description = 'Historial de Jefaturas'
#
#     usuario_id = fields.Many2one(
#         'res.users',
#         string='Jefe',
#         required=True
#     )
#
#     area_id = fields.Many2one(
#         'area',
#         string='Área',
#         required=True
#     )
#
#     fecha_inicio = fields.Date(
#         string='Inicio',
#         required=True
#     )
#
#     fecha_fin = fields.Date(
#         string='Fin'
#     )
#
#     activo = fields.Boolean(
#         string='Vigente',
#         compute='_compute_activo',
#         store=True
#     )
#
#     @api.depends('fecha_inicio', 'fecha_fin')
#     def _compute_activo(self):
#         for record in self:
#             hoy = fields.Date.today()
#             record.activo = (record.fecha_inicio <= hoy) and (not record.fecha_fin or record.fecha_fin >= hoy)