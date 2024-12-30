# -*- coding: utf-8 -*-
import logging
from odoo import models, api, fields

_logging = logging.getLogger()


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    sequence = fields.Integer()


class OuduModeLook(models.Model):
    _name = 'oudu.field.structure'
    _description = '字段查看'

    sequence = fields.Integer()
    priority = fields.Selection([('0', 'Normal'), ('1', 'Urgent')], 'Priority', default='0', index=True)
    name = fields.Char('名称')

    model_id = fields.Many2one('ir.model', string='模型', ondelete="cascade", help="Name of the model")
    field_id = fields.Many2one('ir.model.fields', string='字段', ondelete="cascade", help="字段名称", )
    model_in_model_fields = fields.Many2one('ir.model.fields',
                                            string='模型与模型2关联的字段', ondelete="cascade")
    fields_id = fields.Many2many('ir.model.fields', string='字段', ondelete="cascade")

    model_name = fields.Char(related='model_id.model', string='模型名称')
    field_name = fields.Char(related='field_id.name', string='字段名称')
    relation = fields.Char(related='field_id.relation', string='关联的模型')
    fields_ttype = fields.Selection(related='field_id.ttype', string='字段类型')

    model_id2 = fields.Many2one('ir.model', string='模型2', )
    model_name2 = fields.Char(related='model_id2.model', string='模型名称2')

    field_id2 = fields.Many2one('ir.model.fields', ondelete="cascade", string='模型2与模型关联的字段')
    field_name2 = fields.Char(related='field_id2.name', string='字段名称')
    relation_model2 = fields.Char(related='field_id2.relation', string='关联的模型名称')
    relation_field = fields.Char(related='field_id2.relation_field', string='关联字段')
    fields_ttype3 = fields.Selection(related='field_id2.ttype', string='字段类型')

    @api.onchange('model_in_model_fields')
    def onchange_model_in_model_fields(self):
        if self.model_in_model_fields:
            self.field_id = self.model_in_model_fields
            self.fields_id += self.model_in_model_fields

    @api.onchange('model_id')
    def onchange_model_id(self):
        for res in self:
            if not res.model_id:
                self.all_false(res)
                return
            if res.model_id.model != res.field_id.model:
                self.all_false(res)

            if res.model_name != res.field_id2.relation:
                res.field_id2 = False

            # if res.model_name != res.model_in_model_fields.relation:
            #     res.model_in_model_fields = False

    def all_false(self, res):
        res.field_id = False
        res.model_in_model_fields = False

    @api.onchange('model_id2')
    def onchange_model_id2(self):
        if self.model_name2 != self.field_id2.model:
            self.field_id2 = False
        if self.model_name != self.field_id2.relation:
            self.field_id2 = False
        if self.model_name2 != self.model_in_model_fields.relation:
            self.field_id = False

    @api.onchange('field_id2')
    def onchange_related(self):
        if self.field_id2:
            self.fields_id += self.field_id2

    @api.onchange('field_id')
    def onchange_field_id(self):
        for res in self:
            if res.field_id != res.model_in_model_fields:
                res.model_in_model_fields = False

    def clear_fields_all(self):
        self.fields_id = False
