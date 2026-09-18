from odoo import api, fields, models
from odoo.exceptions import UserError

class UniversalApproval(models.Model):
    _name = 'universal.approval'
    _description = 'Universal Approval Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    res_model = fields.Char(string='Document Model', required=True)
    res_id = fields.Integer(string='Document ID', required=True)
    res_reference = fields.Char(string='Document Reference')
    
    requested_by_id = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user)
    approved_by_id = fields.Many2one('res.users', string='Approved By')
    approval_date = fields.Datetime(string='Approval Date')
    reject_reason = fields.Text(string='Reject Reason')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    def action_approve(self):
        for rec in self:
            rec.write({'state': 'approved', 'approved_by_id': self.env.user.id, 'approval_date': fields.Datetime.now()})

    def action_reject(self):
        # Trigger reject wizard
        pass
