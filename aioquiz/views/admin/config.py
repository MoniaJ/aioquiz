#!/usr/bin/env python3.5
# encoding: utf-8
from sanic.response import json

from views.utils import user_required
from views.utils import HTTPModelClassView
from models import Config


class ConfigView(HTTPModelClassView):
    _cls = Config
    _urls = '/api/admin/config'

    @user_required('admin')
    async def get(self, *_):
        config = await Config.get_by_id(1)
        resp = await config.to_dict()
        return json(resp, sort_keys=True)

    @user_required('admin')
    async def post(self, request, _):
        req = request.json
        try:
            config = await Config.get_by_id(1)
            await config.update_from_dict(req)
        except IndexError:
            config = Config(**req)
            await config.create()
        return json(
            {
                'success': True,
                'msg': 'Config updated'
            },
            sort_keys=True
        )
