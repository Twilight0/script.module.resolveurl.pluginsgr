# -*- coding: utf-8 -*-

'''
    PluginsGR Module
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import json
import re

from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError


class PlaylistGRResolver(ResolveUrl):

    name = 'PlaylistGR'
    domains = ['playlist.gr']
    pattern = r'(?://|\.)(playlist\.gr)/(?:ajax\.php\?action=get_video&id=([\w-]+)|\?id=([\w-]+))'

    def get_media_url(self, host, media_id, subs=False):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        try:
            data = json.loads(res)
            html = data.get('html', res)
        except Exception:
            html = res

        m = re.search(r'''(?:src|href)=["'](?:https?:)?//(?:www\.)?youtube\.com/(?:embed/|watch\?v=)([\w-]+)''', html)
        if m:
            import resolveurl
            return resolveurl.resolve(f'https://www.youtube.com/watch?v={m.group(1)}')

        for src in re.findall(r'''(?:src|href)=["']((?:https?:)?//[^\s"']+)''', html, re.I):
            if src.startswith('//'):
                src = 'https:' + src
            if 'playlist.gr' in src:
                continue
            import resolveurl
            resolved = resolveurl.resolve(src)
            if resolved:
                if subs and not isinstance(resolved, tuple):
                    return resolved, {}
                return resolved

        raise ResolverError('No playable video found.')

    def get_url(self, host, media_id):

        return 'https://playlist.gr/ajax.php?action=get_video&id={0}'.format(media_id)

    @classmethod
    def _is_enabled(cls):
        return True
