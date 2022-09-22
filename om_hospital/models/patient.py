from odoo import api, fields, models, tools, _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "hospital patient"

    name = fields.Char(string='Name', translate=True, tracking=True)
    reference = fields.Char(string='Patient Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Char(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], string="Status",
        default="draft", tracking=True)

    # liste deroulant
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')
    image = fields.Binary(string="Patient Image")
    appointment_lines_id = fields.One2many('hospital.appointment', 'patient_id', string="Appointment")

    #compter le nombre des rendez vous
    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    # les action des buttons
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    # s'execute apres la creation d'un patient
    @api.model
    def create(self, vals):
        if not vals.get("note"):
            vals["note"] = "New Patient"

        # definir la sequence de la reference
        if vals.get('reference', _('Nouveau')) == _('Nouveau'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('Nouveau')
        res = super(HospitalPatient, self).create(vals)
        return res

    # une fonction qui s'execute quand il ya action sur le boutton create
    # usage : modifier les champs de saisie
    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        return res

    # modifier les champs de la liste deroulante
    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + '] ' + rec.name
            result.append((rec.id, name))
        return result

