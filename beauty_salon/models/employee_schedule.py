from odoo import models, fields, api, _


class EmployeeSchedule(models.Model):
    """
    Manages the work schedules of employees in the Beauty Salon. This
    model stores the schedule details such as appointment date, start
    and end times, and the type of service provided.
    """

    _name = 'beauty.salon.employee.schedule'
    _description = 'Beauty Salon Employee Schedule'

    employee_id = fields.Many2one(
        comodel_name='beauty.salon.employee',
        string='Employee', required=True)
    appointment_date = fields.Date()
    appointment_start_time = fields.Float()
    appointment_end_time = fields.Float()
    service_type = fields.Selection([
        ('haircut', 'Haircut'),
        ('nail_care', 'Nail Care'),
        ('massage', 'Massage'),
        ('makeup', 'Makeup')
    ], )

    day_of_week = fields.Selection([
        ('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'),
        ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'),
        ('6', 'Sunday')
    ], string='Day of the Week', compute='_compute_day_of_week', store=True)

    week_type = fields.Selection([
        ('even', 'Even'), ('odd', 'Odd')
    ], compute='_compute_week_type', store=True)

    @api.depends('appointment_date')
    def _compute_day_of_week(self):
        """
        Computes the day of the week for the schedule based on
        the appointment date.
        """
        for record in self:
            if record.appointment_date:
                record.day_of_week = str(record.appointment_date.weekday())
            else:
                record.day_of_week = False

    @api.depends('appointment_date')
    def _compute_week_type(self):
        """
        Determines whether the week of the appointment
         is an 'even' or 'odd' week.
        """
        for record in self:
            if record.appointment_date:
                week_number = record.appointment_date.isocalendar()[1]
                record.week_type = 'even' if week_number % 2 == 0 else 'odd'
            else:
                record.week_type = False

    def action_show_reschedule_wizard(self):
        """
        Opens a wizard that allows rescheduling of the employee's work time.
        Ensures that this action is performed only on a single record.
        """
        self.ensure_one()
        return {
            'name': _('Reschedule Working Time'),
            'type': 'ir.actions.act_window',
            'res_model': 'beauty.salon.employee.reschedule.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_schedule_id': self.id,
                'form_view_initial_mode': 'edit',
            },
        }

    @api.model
    def print_employee_schedule_report(self, *args, **kwargs):
        report = self.env.ref('beauty_salon.action_report_employee_schedule')

        return report.report_action(self)
