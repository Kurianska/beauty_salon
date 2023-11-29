from odoo import fields, models


class PersonMixin(models.AbstractModel):
    """   An abstract model (mixin) that provides common fields for
    person-like entities in the Beauty Salon system. This mixin can
    be inherited by other models that require basic personal information
    fields such as name, contact details, gender, and image."""

    _name = 'person.mixin'
    _description = 'Beauty Salon Person Mixin'

    name = fields.Char(
        string='Person Name', required=True)

    active = fields.Boolean(
        default=True, )
    phone = fields.Char(required=True, )
    email = fields.Char(required=True, )
    address = fields.Char()
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female')
    ], default='male')
    image = fields.Image()
