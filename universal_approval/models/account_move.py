from odoo import api, fields, models
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    approval_status = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Approval Status', copy=False, tracking=True)
    
    def action_submit_for_approval(self):
        for rec in self:
            self.env['universal.approval'].create({
                'res_model': 'account.move',
                'res_id': rec.id,
                'res_reference': rec.name,
                'state': 'pending'
            })
            rec.approval_status = 'pending'

    def action_approve_document(self):
        for rec in self:
            approval = self.env['universal.approval'].search([('res_model', '=', 'account.move'), ('res_id', '=', rec.id), ('state', '=', 'pending')], limit=1)
            if approval:
                approval.action_approve()
            rec.approval_status = 'approved'

    def action_reject_document(self):
        for rec in self:
            approval = self.env['universal.approval'].search([('res_model', '=', 'account.move'), ('res_id', '=', rec.id), ('state', '=', 'pending')], limit=1)
            if approval:
                approval.write({'state': 'rejected'})
            rec.approval_status = 'rejected'
