# -*- coding: utf-8 -*-
"""
ResolveURL Test Suite Harness
Mocks the Kodi environment and loads ResolveURL modules for standalone testing.
"""

import os
import sys
import types

# Ensure temp resources exist for ResolveURL settings initialization
os.makedirs('/tmp/resources', exist_ok=True)
for path in ['/tmp/settings.xml', '/tmp/resources/settings.xml']:
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write('<settings></settings>')


class MockWindowXMLDialog:
    pass


class MockWindowDialog:
    pass


def make_mod(name, **attrs):
    m = types.ModuleType(name)
    m.__all__ = list(attrs.keys())
    for k, v in attrs.items():
        setattr(m, k, v)
    return m


class MockAddon:
    def __init__(self, id=None):
        self.id = id or 'script.module.resolveurl'

    def getAddonInfo(self, attr):
        if attr == 'version':
            return '21.0.0'
        return '/tmp'

    def getSetting(self, key):
        return ''

    def setSetting(self, key, value):
        pass

    def getLocalizedString(self, id):
        return ''

    def openSettings(self):
        pass


class MockDialog:
    def __init__(self, *a, **k):
        pass

    def notification(self, *a, **k):
        pass


# Set up mock Kodi native C/Python modules
xbmc = make_mod(
    'xbmc',
    LOGINFO=1,
    LOGERROR=2,
    LOGWARNING=3,
    LOGNOTICE=4,
    LOGDEBUG=5,
    log=lambda *a, **k: None,
    translatePath=lambda p: p,
    executeJSONRPC=lambda cmd: '{"result":{"Debug.showloginfo":false}}',
    getInfoLabel=lambda l: '',
    sleep=lambda ms: None,
    getSupportedMedia=lambda m: '.mp4|.mkv|.avi|.m3u8',
    getCondVisibility=lambda s: True,
)

xbmcgui = make_mod(
    'xbmcgui',
    Dialog=MockDialog,
    ListItem=lambda *a, **k: None,
    WindowXMLDialog=MockWindowXMLDialog,
    WindowDialog=MockWindowDialog,
)

xbmcplugin = make_mod(
    'xbmcplugin',
    setResolvedUrl=lambda *a, **k: None,
)

xbmcvfs = make_mod(
    'xbmcvfs',
    exists=lambda p: True,
    mkdir=lambda p: None,
    mkdirs=lambda p: None,
    File=lambda *a, **k: None,
    translatePath=lambda p: p,
)

xbmcaddon = make_mod(
    'xbmcaddon',
    Addon=MockAddon,
)

sys.modules['xbmc'] = xbmc
sys.modules['xbmcgui'] = xbmcgui
sys.modules['xbmcplugin'] = xbmcplugin
sys.modules['xbmcvfs'] = xbmcvfs
sys.modules['xbmcaddon'] = xbmcaddon

# Configure sys.path for local Kodi libraries and plugins
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.join(REPO_ROOT, 'resources', 'plugins')

resolveurl_search_paths = [
    '/home/twilight/Development/Kodi_libs/script.module.kodi-six/libs',
    '/home/twilight/Development/Kodi_libs/ResolveURL/script.module.resolveurl/lib',
    PLUGINS_DIR,
]

for p in resolveurl_search_paths:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)
