from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Asset(models.Model):
    _name = 'soe_fixed_assets.asset'
    _description = 'soe_fixed_assets.asset'

    code = fields.Char(string="Código", required=True, help="Escriba el código del activo fijo")

    acquisition_id = fields.Many2one(
        "soe_fixed_assets.acquisition",  #TODO: CAMBIAR EL NOMBRE DEL IDENTIFICADOR
        string="Nro Acta de Recepcion",
        help="Seleccione el acta de Recepcion"
    )

    area_id = fields.Many2one(
        "soe_fixed_assets.area",
        string="Area",
        help="Seleccione el area",
        required=True
    )

    group_id = fields.Many2one(
        "soe_fixed_assets.group",
        string="Grupo",
        help="Seleccione el grupo",
        required=True
    )

    measure_id = fields.Many2one("soe_fixed_assets.measure", string="Medida",
        help="Seleccione la medida", required=True)

    quality_id = fields.Many2one("soe_fixed_assets.quality", string="Calidad",
        help="Seleccione la calidad", required=True)

    manager_id = fields.Char(string="Encargado", required=True,
        help="Seleccione el encargado del activo fijo")

    name = fields.Char(string="Nombre", required=True, help="Escriba el nombre del activo fijo")

    description = fields.Char(string="Descripcion", required=True, help="Escriba la descripcion del activo fijo")

    brand = fields.Char(string="Marca", required=True, help="Escriba la marca del activo fijo")

    cost = fields.Float(string="Costo", required=True, help="Escriba el costo del activo fijo")

    asset_loan_id = fields.Many2one("soe_fixed_assets.asset_loans", string="Prestamo",
        help="")

    _sql_constraints = [
        ('unique_acquisition', 'unique(acquisition_id)', 'Esta Acta de Recepcion pertenece a otro activo fijo'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """
        Sobrescribe el método create para asegurar que acquisition_id sea requerido,
        y delega la actualización del acquisition_id al método write.
        """
        for vals in vals_list:
            if not vals.get('acquisition_id'):
                raise UserError(_("No se puede crear un Activo Fijo sin un Acta de Recepción asociada."))
        # Llama al create original para crear el activo
        new_assets = super().create(vals_list)
        # Actualiza el acquisition_id en la acquisition correspondiente
        for new_asset in new_assets:
            new_asset.acquisition_id.write({'asset_id': new_asset.id})
        return new_assets

    def write(self, vals):
        """
        Sobrescribe el método write para evitar problemas de herencia y recursividad.
        """
        super().write(vals)
        return True

    def action_ver_acta(self):
        """
        Este método abre la vista formulario del acta de recepción relacionada con el activo fijo.
        """
        self.ensure_one()  # Asegura que self es un solo registro
        return {
            'type': 'ir.actions.act_window',
            'name': 'Acta de Recepción',
            'view_mode': 'form',
            'res_model': 'soe_fixed_assets.acquisition',
            'res_id': self.acquisition_id.id,  # Abre el registro específico del acta
            'target': 'current',  # La vista se abre en la misma ventana
        }