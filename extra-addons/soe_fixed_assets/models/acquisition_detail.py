from odoo import models, fields, api

class AcquisitionDetail(models.Model):
    _name = 'soe_fixed_assets.acquisition_detail'
    _description = 'Detail of Acquisition'

    asset_id = fields.One2many(
        "soe_fixed_assets.asset",
        "acquisition_detail_id",
        string = "Activos fijos",
        required=True
    )

    acquisition_id = fields.Many2one(
        "soe_fixed_assets.acquisition",
        string = "Activos fijos documento alta",
        required=True,
    )

    # asset_code = fields.Char(
    #     'asset_id.code',
    #     string="Codigo",
    #     required=True
    # )
    # asset_brand = fields.Char(
    #     'asset_id.brand',
    #     string="Marca",
    #     required=True
    # )
    # asset_description = fields.Char(
    #     'asset_id.description',
    #     string="Descripcion",
    #     required=True
    # )
    # asset_quality = fields.Char(
    #     'asset_id.quality',
    #     string="Calidad",
    #     required=True
    # )
    comments = fields.Text(
        string="Comentarios",
    )