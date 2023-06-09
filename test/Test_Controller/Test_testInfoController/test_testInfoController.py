#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from utils.response_code import RET
from .datas import add_datas,get_datas,delete_datas,update_datas,addlist_datas
from controller.testInfoController import TestInfoController


@pytest.mark.controller
def test_add():
    for data in add_datas:
        result = TestInfoController.add(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_get():
    for data in get_datas:
        result = TestInfoController.get(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_delete():
    for data in delete_datas:
        result = TestInfoController.delete(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_update():
    for data in update_datas:
        result = TestInfoController.update(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_addlist():
    for data in addlist_datas:
        result = TestInfoController.add_list(**data)
        assert result['code'] == RET.OK