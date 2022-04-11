#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import weixinapp_blueprint
from .weixinappResource import WeixinappResource

api = Api(weixinapp_blueprint)

api.add_resource(WeixinappResource, '/weixinapp', endpoint='weixinapp')


@weixinapp_blueprint.route('/weixinapp/info-collect', methods=['POST'], endpoint='info-collect')
def Info_collect():
    return WeixinappResource.infomation_collection()


@weixinapp_blueprint.route('/weixinapp/pic_upload', methods=['POST'], endpoint='pic_upload')
def Pic_upload():
    return WeixinappResource.Pic_upload()
