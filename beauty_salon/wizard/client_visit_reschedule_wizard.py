from odoo import models, fields, exceptions, _


class ClientVisitRescheduleWizard(models.TransientModel):
    """
    A transient model used for rescheduling or canceling a client's visit
    in the Beauty Salon system. This wizard allows users to modify the date,
    start and end times of a visit, or to cancel it entirely.
    """
    _name = 'client.visit.reschedule.wizard'
    _description = 'Reschedule or Cancel Client Visit'

    visit_id = fields.Many2one(
        'beauty.salon.client.visit',
        string='Visit',
        required=True)
    new_visit_date = fields.Date()
    new_visit_start_time = fields.Float()
    new_visit_end_time = fields.Float()
    new_employee_id = fields.Many2one(
        'beauty.salon.employee',
        string='New Employee')
    new_client_id = fields.Many2one(
        'beauty.salon.client',
        string='New Employee')
    cancel_visit = fields.Boolean()

    def action_reschedule_or_cancel(self):
        """
        Reschedules or cancels a client visit based on the user's input.
        Raises a UserError if attempting to reschedule or cancel on the day
        of the appointment.
        """
        self.ensure_one()
        visit = self.visit_id

        if fields.Date.today() >= visit.visit_date:
            raise exceptions.UserError(_("Cannot reschedule or cancel "
                                         "the visit on the day "
                                         "of the appointment."))

        if self.cancel_visit:
            visit.unlink()
        else:
            if self.new_visit_date:
                visit.visit_date = self.new_visit_date
            if self.new_visit_start_time:
                visit.visit_start_time = self.new_visit_start_time
            if self.new_visit_end_time:
                visit.visit_end_time = self.new_visit_end_time
            if self.new_employee_id:
                visit.employee_id = self.new_employee_id
            visit.state = 'draft'
