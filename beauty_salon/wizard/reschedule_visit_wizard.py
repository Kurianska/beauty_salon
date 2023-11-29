from odoo import models, fields


class EmployeeRescheduleWizard(models.TransientModel):
    _name = 'beauty.salon.employee.reschedule.wizard'
    _description = 'Beauty Salon Employee Reschedule Wizard'

    schedule_id = fields.Many2one(
        comodel_name='beauty.salon.employee.schedule',
        string="Schedule"
    )
    new_date = fields.Date()
    new_start_time = fields.Char()
    new_end_time = fields.Char()
    new_employee_id = fields.Many2one(
        comodel_name='beauty.salon.employee',
        string="New Employee"
    )

    def action_reschedule(self):
        self.ensure_one()
        self.schedule_id.unlink()
        self.env['beauty.salon.employee.schedule'].create({
            'employee_id':
                self.new_employee_id.id or self.schedule_id.employee_id.id,
            'appointment_date':
                self.new_date or self.schedule_id.appointment_date,
            'appointment_start_time':
                self.new_start_time or self.schedule_id.appointment_start_time,
            'appointment_end_time':
                self.new_end_time or self.schedule_id.appointment_end_time,
        })

        return {'type': 'ir.actions.act_window_close'}
