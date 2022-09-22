from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "hospital Appointment"
    # _order = "id desc"

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string="Patient")  # liste deroulant
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")  # liste deroulant
    age = fields.Char(string="Age", related="patient_id.age", tracking=True)  # recuperation de la donnee par l'id
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], required=True, default='male', tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], string="Status",
        default="draft", tracking=True)
    note = fields.Text(string='Description', tracking=True)
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="check Up Time")
    prescription = fields.Text(string="Prescription")
    prescription_lines_id = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                            string="Prescriptions Lines")

    # les action des buttons
    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    # une fonction qui s'execute quand on cree un rendez vous
    @api.model
    def create(self, vals):
        if not vals.get("note"):
            vals["note"] = "New Patient"

        # definir la sequence de la reference
        if vals.get('name', _('Nouveau')) == _('Nouveau'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('Nouveau')
        res = super(HospitalAppointment, self).create(vals)
        return res

    # une fonction qui s'execute quant on change la valeur du champ
    # Remplir les champs automatiquement en se referant de l'id de l'objet
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = ''

    # empecher la suppression si le state est a done
    def unlink(self):
        if self.state == 'done':
            raise ValidationError("You Cannot Delete %s as it is in Done" % self.name)
        return super(HospitalAppointment, self).unlink()


# class Appointment Prescription Lines
class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
