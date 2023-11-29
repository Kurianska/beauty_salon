from odoo import models, fields, api, exceptions, _


class Employee(models.Model):
    """
    Represents an employee within a beauty salon. This model extends
    the person.mixin model and includes fields for managing
    employee-specific data such as specialty, role, mentor/intern
    relationships, client relations, and work schedules.
    """
    _name = 'beauty.salon.employee'
    _description = 'Beauty Salon Employee'
    _inherit = ['person.mixin']

    name = fields.Char(
        string="Employee Name", index=True, required=True)
    active = fields.Boolean(
        default=True, )
    passport_data = fields.Char(
        string='Client Passport Data', required=True)
    specialty = fields.Selection([
        ('hair_stylist', 'Hair Stylist'),
        ('nail_technician', 'Nail Technician'),
        ('massage_therapist', 'Massage Therapist'),
        ('makeup_artist', 'Makeup Artist')
    ], required=True)

    client_ids = fields.Many2many(comodel_name='beauty.salon.client',
                                  string='Clients')
    role = fields.Selection([
        ('mentor', 'Mentor'),
        ('intern', 'Intern'),
        ('none', 'None')
    ], default='none', required=True)

    mentor_id = fields.Many2one(
        comodel_name='beauty.salon.employee',
        string='Mentor',
        domain=[('role', '=', 'mentor')])
    intern_ids = fields.One2many(comodel_name='beauty.salon.employee',
                                 inverse_name='mentor_id',
                                 string='Interns',
                                 domain=[('role', '=', 'intern')])

    visit_ids = fields.One2many(
        comodel_name='beauty.salon.client.visit',
        inverse_name='employee_id',
        string='Client Visits')

    schedules_ids = fields.One2many(
        comodel_name='beauty.salon.employee.schedule',
        inverse_name='employee_id',
        string='Schedules')

    @api.constrains('role', 'mentor_id')
    def _check_mentor_for_intern(self):
        """
        Ensures that every intern (role == 'intern') has a mentor assigned.
        Raises a ValidationError if an intern does not have a mentor.
        """
        for record in self:
            if record.role == 'intern' and not record.mentor_id:
                raise exceptions.ValidationError(
                    _("Interns must have a mentor assigned."))
