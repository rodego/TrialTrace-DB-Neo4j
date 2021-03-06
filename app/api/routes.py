from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
from ..tasks.tasks import *
import json



api = Blueprint('api', __name__, url_prefix='/api')
rest = Api(api)


class Example(Resource):
  def get(self):

    data = []
    trials = show_trials()
    for trial in trials:
      datapoints = show_trial_data(trial.trial_id)
      row = {}
      for datapoint in datapoints:
        value = str(datapoint.datum_value)
        field = str(datapoint.datum_belongs_to_field)
        cell =  {field : value}
        row.update(cell)
      data.append(row)

      fields = []
      all_fields = retrieve_fields_from_db()
      for field in all_fields:
        if field.field_include:
          name = str(field.field_name)
          field_id = str(field.field_uid)
          cell =  {field_id : name}
          fields.append(cell)        
    # print(fields)
    return {'data': data, 'fields' : fields}



class NewCol(Resource):
  def post(self):
    response = request.json
    print(response)
    add_field_to_db(response)
    # pass

rest.add_resource(Example, '/')
rest.add_resource(NewCol, '/newcol')