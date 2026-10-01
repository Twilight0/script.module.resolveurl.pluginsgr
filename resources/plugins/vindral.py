# -*- coding: utf-8 -*-

'''
    PluginsGR Module
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import base64
import json
import re
from six.moves import urllib_parse
import xbmc
import xbmcaddon
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError

logger = common.log_utils.Logger.get_logger(__name__)
logger.disable()


class VindralResolver(ResolveUrl):

    name = 'vindral'
    domains = ['vindral.com']
    pattern = r'(?://|\.)(vindral\.com)/(?:.*?[?&](?:core\.)?channelId=)?([\w-]+)'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}

        if not xbmc.getCondVisibility('System.HasAddon(plugin.video.alivegr)'):
            raise ResolverError('AliveGR addon is required to play Vindral streams.')

        channel_id = media_id
        lb_url = f"https://lb.cdn.vindral.com/api/v4/connect?channelId={channel_id}"
        json_data = self.net.http_GET(lb_url, headers=headers).content
        try:
            lb_json = json.loads(json_data)
        except Exception as e:
            raise ResolverError(f'Failed to parse Vindral load balancer response: {e}')

        edges = lb_json.get('edges')
        if not edges:
            raise ResolverError('No edges found in Vindral response.')

        edge = edges[0]
        url = ''.join(
            [
                edge, '/subscribe?channelId=', channel_id,
                '&audio.codec=aac&audio.bitRate=128000&video.codec=h264&video.width=1280&video.height=720&video.bitRate=3000000&burstMs=2000'
            ]
        )

        logger.log_notice(f'VINDRAL_PROXY_URL: {url}')

        ws_b64 = base64.urlsafe_b64encode(url.encode('utf-8')).decode('utf-8')
        port = xbmcaddon.Addon('plugin.video.alivegr').getSetting('proxy_port') or '50199'
        origin = urllib_parse.quote('https://www.megatv.com')

        return 'http://127.0.0.1:{port}/mega.flv?ws={ws_b64}&origin={origin}'.format(
            port=port, ws_b64=ws_b64, origin=origin
        )

    def get_url(self, host, media_id):
        return f'https://lb.cdn.{host}/api/v4/connect?channelId={media_id}'

    @classmethod
    def _is_enabled(cls):
        return True
