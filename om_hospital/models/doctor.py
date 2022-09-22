from odoo import api, fields, models, tools, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "hospital doctor"
    _rec_name = 'doctor_name'
    # _order = 'doctor_name'
    # _rec_name = 'age' recupere l'age sur la liste deroulante

    doctor_name = fields.Char(string='Name', translate=True, tracking=True)
    age = fields.Char(string='Age', tracking=True, copy=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    image = fields.Binary(Stringe="Doctor Image")

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s (Copy)", self.doctor_name)
        default['note'] = "Copied Record"
        return super(HospitalDoctor, self).copy(default)
