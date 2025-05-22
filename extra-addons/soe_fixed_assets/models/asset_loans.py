from odoo import models, fields, api, _

class AssetsLoan(models.Model):
    _name = 'soe_fixed_assets.asset_loans'
    _description = 'soe_fixed_assets.asset_loans'

    nro_cite = fields.Char( string="Nro Cite", required=True)
    loan_date_ini = fields.Date(string="Fecha de prestamo", required=True, help="Fecha de prestamo del activo fijo")
    loan_date_end = fields.Date(string="Valor de prueba", help="Fecha de devolucion del activo fijo")
    destiny = fields.Char(string="Destino del prestamo", required=True)
    manager = fields.Char(string="Persona que recibe", required=True)

    asset_loans_detail_ids = fields.One2many(
        "soe_fixed_assets.asset_loans_detail",
        "asset_loans_id",
        string="Detalles del prestamo",
        copy=True)

    #@api.model
    #def create(self, vals):
    #    if vals.get('name', _('Nuevo')) == _('Nuevo'):
    #        vals['name'] = self.env['ir.sequence'].next_by_code('soe.fixed.assets.loan.sequence') or _('Nuevo')
    #    return super(AssetsLoan, self).create(vals)