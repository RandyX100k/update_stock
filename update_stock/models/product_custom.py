# -*- coding:utf-8 -*-
from  odoo import  models , fields,api

class ProductProduct(models.Model):
    _inherit = "product.product"


    product_update_id = fields.Many2one("update.stock",string="Update_id")
    qty = fields.Integer(string="QTY")

    @api.model
    def create(self, vals):
        if not vals.get("barcode"):
            seq = self.env["ir.sequence"]
            seq_next = seq.next_by_code("update.barcode")
            vals["barcode"] = seq_next or "/"


        return super().create(vals)
