from datetime import timedelta
from odoo import models, api, fields


class BeautySalonService(models.Model):
    _name = 'beauty.salon.service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    last_visit_date = fields.Date()
    client_id = fields.Many2one('res.partner', string='Client')

    @api.model
    def send_service_reminder(self):
        reminder_date = fields.Date.today() - timedelta(days=30)
        services_to_remind = (
            self.search([(
                'last_visit_date', '<', reminder_date)]))

        template = self.env.ref(
            'beauty_salon.beauty_salon_service_reminder_email_template')

        for service in services_to_remind:
            if service.client_id.email:
                template.send_mail(service.id, force_send=True)

    def _send_service_reminder(self):
        target_date = fields.Date.today() - timedelta(days=30)
        clients_to_remind = (
            self.env['beauty.salon.client'].search([
                ('last_visit_date', '<', target_date),
            ]))

        template = self.env.ref(
            'beauty_salon.beauty_salon_service_reminder_email_template')

        for client in clients_to_remind:
            if client.email:
                template.send_mail(client.id, force_send=True)
