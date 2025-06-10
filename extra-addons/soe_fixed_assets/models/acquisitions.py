from odoo import models, fields, api

class Acquisition(models.Model):
    _name = 'soe_fixed_assets.acquisition'
    _description = 'soe_fixed_assets.acquisition'


    acquisition_detail_id = fields.One2many(
        'soe_fixed_assets.acquisition_detail',
        'acquisition_id',
        string='Detalle del Acta de Activos Fijos',
    )

    nro_cite = fields.Char(
        string="Nro de Acta de Recepcion ",
        required=True, help="Escriba el numero de cite",
        regex=r'^\d{4}/20\d{2}$'
    ) #TODO: Comprobar la validacion de la expresion regular

    pdf_file = fields.Binary(
        string='Archivo PDF',
        required=True,
        attachment=True
    )
    pdf_name = fields.Char(
        string="Archivo PDF del acta de entrega del activo fijo ",
        required=True,
        help="Cargue la imagen del acta de entrega del activo fijo"
    )
    date_received = fields.Date(
        string="Fecha de recepción",
        required=True,
        help="Fecha de recepción del activo",
        default=fields.Date.today
    )

    acquisition_type = fields.Selection([
        ('reasignacion', 'Reasignación'),
        ('compra', 'Compra'),
    ],  string="Tipo",
        help="Seleccione el tipo de alta de activos fijo que corresponda",
        required=True,
    )

    can_add_multiple_details = fields.Boolean(
        string="Permitir Múltiples Detalles",
        compute="_compute_can_add_multiple_details",
        store=False,
    )

    @api.depends('acquisition_type')
    def _compute_can_add_multiple_details(self):
        for rec in self:
            # Si el tipo de adquisición es 'reasignacion', permite añadir múltiples detalles
            rec.can_add_multiple_details = (rec.acquisition_type == 'reasignacion')

    _sql_constraints = [
        ('unique_cite', 'unique(nro_cite)', 'El Nro de Cite debe ser unico'),
        # ('unique_asset', 'unique(asset_id)', 'Este activo fijo ya fue vinculado a otra acta de recepcion'),
        ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            nro_cite = vals.get('nro_cite')

            vals['nro_cite'] = f"Acta de Recepcion {nro_cite}"
            if 'pdf_file' in vals and 'nro_cite' in vals:
                file_content = vals.get('pdf_file')
                if file_content and nro_cite:
                    vals['pdf_name'] = f"{nro_cite}.pdf"
        return super().create(vals_list)

    @api.model
    def write(self, vals):
        if 'pdf_file' in vals and self.nro_cite and 'pdf_name' not in vals:
            file_content = vals.get('pdf_file')
            nro_cite = self.nro_cite
            if file_content and nro_cite:
                vals['pdf_name'] = f"{nro_cite}.pdf"
        return super().write(vals)

    # def action_registrar_activo_fijo(self):
    #     self.ensure_one()
    #     return {
    #         'name': 'Registrar Activo Fijo',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'soe_fixed_assets.asset',
    #         'view_mode': 'form',
    #         'context': {'default_acquisition_id': self.id},  # Pasar el ID del acta al formulario del activo
    #         'target': 'new',
    #     }

