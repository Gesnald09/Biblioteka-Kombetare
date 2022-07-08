from odoo import fields, models, api
from datetime import datetime,date,time,timedelta

class LibrariKartela(models.Model):
    _name = 'librari.kartela'
    _description = 'Description'

    emri=fields.Text(string="Emri", required=True)
    mbiemri  = fields.Text(string="Mbiemri",required=False)
    nr_id = fields.Text(string="Numri personal ID",required=True)
    ditelindja = fields.Date(string='Ditelindja',required=True)
    telefoni = fields.Text(string='Telefoni', required=True)
    email = fields.Text(string='Email',required=True)
    adresa = fields.Text(string='Adresa',required=True)
    kategoria  = fields.Selection(string='Kategoria',selection=[('Nxenes', 'Nxenes'),('Student', 'Student'), ('Mesues','Mesues'),('Qytetar','Qytetar'),],required=True, )
    liberiri_ids  = fields.One2many(comodel_name='librari.liberiri',inverse_name='kartela_id',string='Id e karteles',required=True)

class LibrariLiberiri(models.Model):
    _name = 'librari.liberiri'
    _description = 'Description'

    '''name  = fields.Char(string='Emri i Karteles',required=True)'''
    emri_i_librit1   = fields.Many2one(comodel_name='librari.librat',string='Titulli i librit',required=True)
    kartela_id  = fields.Many2one(comodel_name='librari.kartela',string='Vendosni id te antarit',required=False)
    data_e_marrjes  = fields.Date(string='Vendosni daten e marrjes',required=True,default=fields.Date.today)
    data_e_kthimit  = fields.Date(string='Data e kthimit',required=False,compute="_compute_data_e_kthimit",
                                 inverse="_inverse_data_e_kthimit")
    kohezgjatja  = fields.Integer(string='Kohezgjatja',default=1)
    state = fields.Selection([('padorezuar','Pa dorezuar'),('dorezuar','Dorezuar')],default='padorezuar',String='Status')
    emri_i_punonjesit =fields.Many2one(comodel_name='librari.punonjesitemarrdhenievemepublikun',
                                       string='Emri i punonjesit ne momentin e marrjes se librit',
                                       required=True)
    emri_i_punonjesit = fields.Many2one(comodel_name='librari.punonjesitemarrdhenievemepublikun',
                                        string='Emri i punonjesit ne momentin e dorezimit se librit',
                                        required=False)
    def dorezoj(self):
        self.state='dorezuar'


    @api.multi
    @api.depends('data_e_marrjes','kohezgjatja')
    def _compute_data_e_kthimit(self):
        for record in self:
            if not (record.data_e_marrjes and record.kohezgjatja):
                record.data_e_kthimit=record.data_e_marrjes
            else:
                kohezgjatja = timedelta(days=record.kohezgjatja-1)
                record.data_e_kthimit=fields.Date.to_string(fields.Date.from_string(record.data_e_marrjes)+kohezgjatja)

    @api.multi
    @api.depends('data_e_marrjes', 'data_e_kthimit')
    def _inverse_data_e_kthimit(self):
        for record in self:
            if record.data_e_marrjes and record.data_e_kthimit:
                record.kohezgjatja=(fields.Date.from_string(record.data_e_kthimit)-fields.Date.from_string(record.data_e_marrjes)).days+1
            else:
                continue

    class LibrariLibrat(models.Model):
        _name = 'librari.librat'
        _rec_name = 'emri_i_librit1'
        _description = 'Description'

        emri_i_librit1  = fields.Text(string="Emri i librit",required=True)
        autori_i_librit  = fields.Text(string="Autori i librit",required=True)
        emri_i_shtepise_botuese = fields.Many2one(comodel_name='librari.furnitori', string='Shtepia Botuese', required=True)
        viti_i_prodhimit  = fields.Text(string="Vitin i botimit",required=True)
        cmimi_i_librit  = fields.Float("Cmimi i librit",default=0.00)
        numri_i_kopjeve  = fields.Integer("Numri i kopjeve per kete liber",default=0.00)
        shuma_per_tu_paguar  = fields.Float("Shuma per tu paguar",compute='_onchange_shuma_per_tu_paguar',default=0.00)
        foto_e_librit  = fields.Binary(string="Foto e librit")
        liberiri_ids = fields.One2many(comodel_name='librari.liberiri', inverse_name='emri_i_librit1',required=True)

        @api.multi
        @api.depends('cmimi_i_librit','numri_i_kopjeve')
        def _onchange_shuma_per_tu_paguar(self):
            for rec in self:
                rec.shuma_per_tu_paguar=rec.cmimi_i_librit * rec.numri_i_kopjeve

    class LibrariFurnitori(models.Model):
        _name = 'librari.furnitori'
        _rec_name='emri_i_shtepise_botuese'
        _description = 'Description'

        emri_i_shtepise_botuese=fields.Text(string="Shtepia Botuese",required=True)


class LibrariPunonjesi(models.Model):
    _name = 'librari.punonjesi'
    _rec_name = 'emri_i_punonjesit'
    _description = 'Description'

    emri_i_punonjesit  = fields.Text(string="Emri i Punonjesit",required=True)
    mbiemri_i_punonjesit  = fields.Text(string="Mbiemri i Punonjesit",required=True)
    ditelindja  = fields.Date(string='Ditelindja e Punonjesit',required=True)
    adresa_e_punonjesit  = fields.Text(string="Adresa e Punonjesit",required=True)
    numri_i_telefonit  = fields.Text(string="Numri i telefonit te punonjesit",required=True)
    email_i_punonjesit  = fields.Text(string="Email i punonjesit",required=True)
    pozicioni = fields.Many2one(comodel_name='librari.pozicioni', string='Pozicioni i Punonjesit', required=True)


class LibrariPozicioni(models.Model):
    _name = 'librari.pozicioni'
    _rec_name = 'pozicioni'
    _description = 'Description'

    pozicioni  = fields.Text(string="Pozicioni i Punonjesit",required=True)
    pagesa_per_kete_pozicion  = fields.Float(string='Paga per kete Pozicion',required=True,default=0.00)


class LibrariPunonjesitemarrdhenievemepublikun(models.Model):
    _name = 'librari.punonjesitemarrdhenievemepublikun'
    _rec_name = 'emri_i_punonjesit'
    _description = 'Description'

    emri_i_punonjesit = fields.Many2one(comodel_name='librari.punonjesi', string='Emri i Punonjesit', required=True)


