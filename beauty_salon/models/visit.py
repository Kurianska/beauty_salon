from datetime import datetime
from odoo import models, fields, exceptions, api, _


class ClientVisit(models.Model):
    """Represents a client's visit to the beauty salon. This model
     stores details about each visit, including the date, start and
     end time, assigned employee, client, service type, and the visit's
     current status."""

    _name = 'beauty.salon.client.visit'
    _description = 'Beauty Salon Client Visit'

    active = fields.Boolean(
        default=True, )
    visit_date = fields.Date(required=True)
    visit_start_time = fields.Float()
    visit_end_time = fields.Float()
    employee_id = fields.Many2one(
        comodel_name='beauty.salon.employee',
        string='Employee')
    client_id = fields.Many2one(
        comodel_name='beauty.salon.client',
        string='Client')
    service_type = fields.Selection([
        ('haircut', 'Haircut'),
        ('nail_care', 'Nail Care'),
        ('massage', 'Massage'),
        ('makeup', 'Makeup')
    ], required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], default='draft', string='Status')

    @api.constrains('visit_date', 'visit_start_time',
                    'visit_end_time', 'employee_id')
    def _check_schedule_availability(self):
        """
        Checks the availability of the employee's schedule and ensures
        that there are no overlapping visits. Raises a ValidationError
        if the schedule is not available or if there's an overlap with
        other visits.
        """
        for visit in self:

            work_schedule = self.env['beauty.salon.employee.schedule'].search([
                ('employee_id', '=', visit.employee_id.id),
                ('appointment_date', '=', visit.visit_date)
            ])

            if not work_schedule:
                raise exceptions.ValidationError(
                    _("No work schedule available for the selected "
                      "employee on this date."))

            if any(not (
                    visit.visit_start_time >= ws.appointment_start_time
                    and visit.visit_end_time <= ws.appointment_end_time)
                   for ws in work_schedule):
                raise exceptions.ValidationError(
                    _("The visit time is outside the employee's working "
                      "hours."))

            existing_visits = self.env['beauty.salon.client.visit'].search([
                ('employee_id', '=', visit.employee_id.id),
                ('visit_date', '=', visit.visit_date),
                ('id', '!=', visit.id)
            ])

            for other_visit in existing_visits:
                if (
                        visit.visit_start_time
                        < other_visit.visit_end_time
                        and visit.visit_end_time
                        > other_visit.visit_start_time):
                    raise exceptions.ValidationError(
                        _("There is an overlapping client visit during "
                          "the specified time."))

    @api.model
    def _update_visit_status(self):
        """
        Automatically updates the status of the visit based on
        the current date and time. Marks visits as 'done' if
        the visit date is in the past.
        """
        current_date = fields.Date.today()
        current_time = datetime.now().hour + datetime.now().minute / 60.0

        for visit in self.search([('state', '!=', 'done')]):
            if visit.visit_date < current_date or \
                    (visit.visit_date == current_date
                     and visit.visit_end_time <= current_time):
                visit.write({'state': 'done'})
            elif (visit.visit_date == current_date
                  and visit.visit_start_time <= current_time
                  < visit.visit_end_time):
                visit.write({'state': 'confirmed'})

    def action_show_reschedule_wizard(self):
        """
        Opens a wizard that allows rescheduling or cancelling of the visit.
        Ensures that this action is only performed on a single record.
        """
        self.ensure_one()
        return {
            'name': _('Reschedule or Cancel Visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'client.visit.reschedule.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_visit_id': self.id,
            },
        }
