from odoo import fields, models
class UniversalRejectWizard(models.TransientModel):
    _name = 'universal.reject.wizard'
    _description = 'Universal Reject Wizard'
    
    reason = fields.Text('Reason for Rejection', required=True)
    approval_id = fields.Many2one('universal.approval', 'Approval Request')
