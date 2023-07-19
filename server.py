#from __future__ import print_function,unicode_literals
import aiohttp
import asyncio
import base64
import json
import jwt
import logging
import time
import traceback
import urllib.parse
import uuid

import redis.asyncio as redis

from aiohttp import web
from lib.settings import Settings, LogRecord, CustomFormatter

redis_conn = redis.Redis(host=Settings.redis_host, port=Settings.redis_port, decode_responses=True)

logging.setLogRecordFactory(LogRecord)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


def html_response(document):
    with open('static/html/{0}'.format(document), "r") as d:
        return web.Response(text=d.read(), content_type='text/html')

async def main(request):
    logger.info('main hit.')
    return html_response('index.html')

def generate_guest_link(username, address):
    payload = {"sub": username+address, "name" : username, "iss": Settings.iss, "exp":int(time.time()) + 3600}
    logger.debug(payload)
    decoded_secret = base64.b64decode(Settings.secret)
    encoded_jwt = jwt.encode(payload, decoded_secret, algorithm='HS256')
    logger.debug(encoded_jwt)
    session_id = uuid.uuid4().hex
    sdk_url = Settings.embed_url
    address = urllib.parse.quote_plus(address)
    sdk_url += "?destination={0}&token={1}&userType=guest&headerToggle=false&autoDial=true&sessionId={2}&embedSize=desktop".format(address, encoded_jwt, session_id)
    return sdk_url, session_id

def format_set_name(username, address):
    return '{0}-_.._-{1}'.format(username, address)

def calc_expire_seconds():
    return 86400 * Settings.expire_days

async def handle_session(request):
    session_id = request.match_info['session_id']
    print("handle_session:{0}".format(session_id))
    hash_set = await redis_conn.hgetall(session_id)
    sdk_url, session_id = generate_guest_link(hash_set['username'], hash_set['address'])
    expires_in = calc_expire_seconds()
    set_name = format_set_name(hash_set['username'], hash_set['address'])
    await redis_conn.expire(set_name, expires_in, gt=True)
    await redis_conn.expire(session_id, expires_in, gt=True)
    raise web.HTTPFound(sdk_url)

async def join(request):
    """
    POST requests from the UI to update / delete a PMR PIN
    """
    body = await request.json()
    logger.debug(body)
    default_error_msg = "A valid Webex Meeting Number or Address is required."
    try:
        username = body.get('name')
        address = body.get('address')
        if len(address) >= 3:
            if address.isdigit():
                address += "@webex.com"
            logger.debug(address)
            if "@" in address:
                sdk_url, session_id = generate_guest_link(username, address)
                response = {"success": True, "url":sdk_url, "session_id":session_id}
            else:
                response = {"error": default_error_msg}
        else:
            response = {"error": default_error_msg}
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        response = {"error": str(e) }
    return web.Response(text=json.dumps(response))

async def get_link(request):
    """
    POST requests from the UI to update / delete a PMR PIN
    """
    body = await request.json()
    logger.debug(body)
    default_error_msg = "A valid Webex Meeting Number or Address is required."
    try:
        username = body.get('name')
        address = body.get('address')
        if len(address) >= 3:
            if address.isdigit():
                address += "@webex.com"
            logger.debug(address)
            if "@" in address:
                set_name = format_set_name(username, address)
                session_id = await redis_conn.get(set_name)
                print('session_id:{0}'.format(session_id))
                if not session_id:
                    session_id = uuid.uuid4().hex
                    await redis_conn.set(set_name, session_id)
                    await redis_conn.hset(session_id, mapping={"username": username, "address": address})
                    print('new map created for session_id:{0} and set_name:{1}'.format(session_id, set_name))
                expires_in = calc_expire_seconds()
                await redis_conn.expire(set_name, expires_in, gt=True)
                await redis_conn.expire(session_id, expires_in, gt=True)
                url = Settings.host + "/" + session_id
                print(url)
                response = {"success": True, "url":url}
            else:
                response = {"error": default_error_msg}
        else:
            response = {"error": default_error_msg}
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        response = {"error": str(e) }
    return web.Response(text=json.dumps(response))

async def redis_loop():
    while True:
        print(f"Redis Ping successful: {await redis_conn.ping()}")
        await asyncio.sleep(300)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', main)])
    app.add_routes([web.post('/join', join)])
    app.add_routes([web.post('/get-link', get_link)])
    app.add_routes([web.static('/static', 'static')])
    app.add_routes([web.static('/session/static', 'static')])
    app.add_routes([web.get('/session/{session_id:.*}', handle_session)])
    
    loop = asyncio.get_event_loop()
    loop.create_task(redis_loop())
    web.run_app(app, loop=loop, port=Settings.port)

