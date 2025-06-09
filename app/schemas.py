from marshmallow import Schema, fields, validate

class RepuestoSchema(Schema):
    codigo_pieza = fields.Str(required=True, validate=validate.Length(min=1))
    descripcion = fields.Str(required=True)
    precio = fields.Float(required=True)
    stock_min = fields.Int(required=True)
    stock_real = fields.Int(required=True)
    stock_disp = fields.Int(required=True)
