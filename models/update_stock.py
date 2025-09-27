# -*- coding:utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UpdateStock(models.Model):
    _name = "update.stock"

    name = fields.Char(
        string="#",
        copy=False,
        default="Nuevo"
    )

    product_ids = fields.One2many(
        "update.stock.line", "product_update_id", string="Productos"
    )

    location_id = fields.Many2one("stock.location",string="Ubicacion")

    state = fields.Selection([
        ("draft","Borrador"),
        ("done","Hecho"),
    ],
        default="draft")

    def proccess_stock(self):
        if not self.location_id:
            raise ValidationError("Especifica la ubicacion del ajuste")

        for record in self:
            for product in record.product_ids:
                if not product.product_id:
                    continue 
                product_id = product.product_id.id
                qty = product.qty
                location_id = record.location_id.id

                # Buscar el quant
                self._cr.execute("""
                    SELECT id, quantity 
                    FROM stock_quant 
                    WHERE product_id = %s AND location_id = %s
                    LIMIT 1
                """, (product_id, location_id))
                quant = self._cr.fetchone()

                if quant:
                    quant_id, quant_qty = quant
                    # Actualizar cantidad
                    self._cr.execute("""
                        UPDATE stock_quant 
                        SET quantity = %s 
                        WHERE id = %s
                    """, (qty, quant_id))
                else:
                    self._cr.execute("""
                                INSERT INTO stock_quant (
                                    location_id, product_id, quantity, reserved_quantity, company_id, in_date, create_date, write_date
                                ) VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), NOW())
                            """, (
                            location_id,
                            product_id,
                            qty,
                            0.0,
                            self.env.company.id
                        ))

                record.name = self.env["ir.sequence"].next_by_code("update.stock") or "/"
                print(record.name)
                self.state = "done"



class UpdateStockLine(models.Model):
    _name = "update.stock.line"

    product_id = fields.Many2one("product.product", string="Producto")
    barcode = fields.Char(string="Código de barras")
    qty = fields.Integer(string="Cantidad a ajustar", default=1)
    product_update_id = fields.Many2one("update.stock", string="Actualización")

    @api.model
    def create(self, vals):

        if vals.get("barcode") and vals.get("product_update_id"):
            existing = self.search([
                ("product_update_id", "=", vals["product_update_id"]),
                ("barcode", "=", vals["barcode"])
            ], limit=1)

            if existing:
                existing.qty += vals.get("qty", 1) or 1
                return existing

            product = self.env["product.product"].search([("barcode", "=", vals["barcode"])], limit=1)
            if product:
                vals["product_id"] = product.id
            else:
                pass

        return super().create(vals)

    def write(self, vals):
        if "barcode" in vals and vals["barcode"]:
            product = self.env["product.product"].search([("barcode", "=", vals["barcode"])], limit=1)
            if product:
                vals["product_id"] = product.id
            else:
                pass

        return super().write(vals)
