#!/usr/bin/env python3.5
# encoding: utf-8
from collections import defaultdict
import logging

from sanic.response import json

from models import Users
from models import UserReview

from orm import DoesNotExist

from utils import create_uuid

from views.utils import get_user_name
from views.utils import HTTPModelClassView
from views.utils import user_required


class SetOrganiserView(HTTPModelClassView):
    _cls = Users
    _urls = '/api/admin/user/set_organiser'

    @user_required('admin')
    async def post(self, request, current_user):
        req = request.json
        user = await Users.get_by_id(req['uid'])
        if user:
            user.organiser = req['organiser']
            await user.update()
            return json({'success': True})
        return json({'success': False, 'reson': 'wrong token'})


class SetMentorView(HTTPModelClassView):
    _cls = Users
    _urls = '/api/admin/user/set_mentor'

    @user_required('admin')
    async def post(self, request, current_user):
        req = request.json
        user = await Users.get_by_id(req['uid'])
        if user:
            user.mentor = req['mentor']
            await user.update()
            return json({
                'success': True,
                'msg': '{} is {} mentor'.format(user.name, 'now a' if req['mentor'] else 'NOT')
            })
        return json({'success': False, 'msg': 'wrong token'})


class ChangeActiveView(HTTPModelClassView):
    _cls = Users
    _urls = '/api/admin/user/set_active'

    @user_required('admin')
    async def post(self, request, current_user):
        req = request.json
        user = await Users.get_by_id(req['uid'])
        if user:
            user.active = req['active']
            await user.update()
            return json({'success': True})
        return json({'success': False, 'msg': 'wrong token'})


class ReviewAttendeesView(HTTPModelClassView):
    _cls = Users
    _urls = ['/api/admin/user/review']

    @user_required('organiser')
    async def get(self, request, current_user):
        allusers = await Users.get_by_many_field_value(
            admin=False,
            organiser=False
        )
        allreviews = await UserReview.get_all()
        reviews = defaultdict(dict)
        for rev in allreviews:
            reviews[rev.users][rev.reviewer] = {
                'score': rev.score,
                'name': await get_user_name(rev.reviewer)
            }
        users = []
        for u in allusers:
            ud = await u.to_dict(include_soft=True)
            ud.update({'reviews': reviews.get(u.id, {})})
            usr = reviews.get(u.id, {})
            review_amount = len(usr) or 1
            ud['score'] = sum([x.get('score', 0) for _, x in usr.items()]) / review_amount
            users.append(ud)
        users.sort(key=lambda a: a['score'], reverse=True)
        return json(users)

    @user_required('organiser')
    async def post(self, request, current_user):
        req = request.json
        req['reviewer'] = current_user.id
        ur = UserReview(**req)
        if not await ur.create():
            return json({'msg': 'already exists', 'error': True})
        all_ur = await UserReview.get_by_field_value('users', req['users'])
        user = await Users.get_by_id(req['users'])
        new_score = sum(u.score for u in all_ur) / (len(all_ur) or 1)
        user.score = new_score
        await user.update()
        return json({'success': True})

    @user_required('organiser')
    async def put(self, request, current_user):
        try:
            req = request.json
            user = await Users.get_by_id(req['users'])
            user.accepted = req['accept']
            await user.update()
            return json({'success': True})
        except:
            logging.exception('review_put')
            return json({'success': False}, status=500)


# noinspection PyMethodMayBeStatic
class AdminForgotPasswordView(HTTPModelClassView):
    _cls = Users
    _urls = '/api/admin/users/new_password/<email>'

    # noinspection PyUnusedLocal
    @user_required('admin')
    async def get(self, request, current_user, email):
        try:
            user = await Users.get_first_by_many_field_value(email=email)
        except DoesNotExist:
            logging.error(email)
            user = False
        if not user:
            return json({'msg': 'wrong email or user does not exist'})
        password = create_uuid()
        await user.set_password(password)
        await user.update()
        return json({"success": True, "msg": password})