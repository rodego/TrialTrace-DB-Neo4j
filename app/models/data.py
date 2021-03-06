from app.main import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, text
from uuid import uuid4
from app.models.users import *


class Trials(db.Model):
    __tablename__ = "trials"
    trial_id = db.Column(db.VARCHAR(11),primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    last_updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    inclusion = db.Column(db.VARCHAR)
    inclusion_note = db.Column(db.Text)
    def __init__(
        self,
        trial_id,
        last_updated_at,
        inclusion,
        inclusion_note
    ):
        self.trial_id = trial_id
        self.last_updated_at = last_updated_at
        self.inclusion = inclusion
        self.inclusion_note = inclusion_note


class Data(db.Model):
    __tablename__ = "data"
    datum_uid = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4, nullable=False)
    datum_belongs_to_field = db.Column(UUID(as_uuid=True), db.ForeignKey('fields.field_uid'))
    datum_belongs_to_trial = db.Column(db.VARCHAR(11), db.ForeignKey('trials.trial_id'))
    datum_value = db.Column(db.Text)
    datum_note = db.Column(db.Text)
    datum_source = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_uid'))
    datum_depends_on = db.Column(UUID(as_uuid=True), db.ForeignKey('data.datum_uid'))
    
    def __init__(
        self,
        datum_value,
        datum_belongs_to_field,
        datum_belongs_to_trial,
        datum_note,
        datum_source,
        # created_at,
        # created_by,
        # datum_depends_on
    ):
        self.datum_value = datum_value
        self.datum_belongs_to_field = datum_belongs_to_field
        self.datum_belongs_to_trial = datum_belongs_to_trial
        self.datum_note = datum_note
        self.datum_source = datum_source
        # self.created_at = created_at
        # self.created_by = created_by
        # self.datum_depends_on = datum_depends_on


# Database model for fields, as in columns that the data belongs to
class Fields(db.Model):
    __tablename__ = "fields"
    field_uid = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4, nullable=False)
    field_meta = db.Column(db.Text)
    field_name = db.Column(db.Text)
    field_note = db.Column(db.Text)
    field_source = db.Column(db.Text)
    field_include = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_uid'))
    field_depends_on = db.Column(UUID(as_uuid=True), db.ForeignKey('fields.field_uid'))

    #TODO add last modified date + onupdate 
    #TODO add cron job and patch api version 

    def __init__(
        self,
        field_meta,
        field_name,
        field_note,
        field_source,
        # created_by,
        # field_depends_on
    ):
        self.field_meta = field_meta
        self.field_name = field_name
        self.field_note = field_note
        self.field_source = field_source
        # self.created_by = created_by
        # self.field_depends_on = field_depends_on
