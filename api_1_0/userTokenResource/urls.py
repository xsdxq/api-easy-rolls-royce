#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import usertoken_blueprint
from api_1_0.userTokenResource.userTokenResource import UserTokenResource
from api_1_0.userTokenResource.userTokenOtherResource import UserTokenOtherResource

api = Api(usertoken_blueprint)

api.add_resource(UserTokenResource, '/userToken/<int:UserID>', '/userToken', endpoint='userToken')


# joint query
@usertoken_blueprint.route('/userToken/query', methods=['GET'], endpoint='userToken_query')
def UserToken_query():
    return UserTokenOtherResource.joint_query()

