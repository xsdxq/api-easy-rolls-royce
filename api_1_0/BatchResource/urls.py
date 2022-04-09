#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import batch_blueprint
from api_1_0.BatchResource.BatchResource import BatchResource
from api_1_0.BatchResource.BatchOtherResource import BatchOtherResource

api = Api(batch_blueprint)

api.add_resource(BatchResource, '/Batch/<AutoID>', '/Batch', endpoint='Batch')
