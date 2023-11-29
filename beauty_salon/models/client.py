from odoo import models, fields


class Client(models.Model):
    """
    Represents a client in the Beauty Salon system. This model extends
    the person.mixin model to include client-specific data such as their
    birthday, related employee, a list of their visits.
    """

    _name = 'beauty.salon.client'
    _description = 'Beauty Salon Client'
    _inherit = ['person.mixin']

    name = fields.Char(
        string="Client Name", index=True, required=True)
    active = fields.Boolean(
        default=True, )
    birthday_date = fields.Char(
        string='Client Birthday Date', required=True)

    employee_id = fields.Many2one(
        comodel_name='beauty.salon.employee', )

    visit_ids = fields.One2many(
        comodel_name='beauty.salon.client.visit',
        inverse_name='client_id',
        string='Visits')
