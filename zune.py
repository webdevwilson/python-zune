# -*- coding: utf-8 -*-
"""
python-zune is a python module for accessing Zune user data

Example Usage:
zuneCard = ZuneCard('your zune tag here')

Homepage: http://www.goodercode.com

Copyright (c) 2010, Kerry Wilson
License: MIT
"""

import urllib
from xml.dom import minidom

_ZUNE_URL = 'http://social.zune.net/zcard/usercardservice.ashx?zunetag='

class ZuneCard:
    """
    Contains user play data

    Example Usage:
    ZuneCard('your zune tag here')

    Properties:
    - id
    - label
    - firstName
    - status
    - location
    - name
    - location
    - bio
    - totalPlays
    - userId
    - tileBig
    - tileSmall
    - backgroundLarge
    - backgroundSmall
    - badges ZuneBadge[]
    - following ZuneArtist[]
    - favorites ZuneTrack[]
    - recentSpins ZuneTrack[]
    - mostPlayed ZuneArtist[]
    """

    def __init__(self, tag):
        self.tag = tag
        self.refresh()

    def refresh(self):
        self.dom = self._load()
        self._node = self.dom.getElementsByTagName('user')[0]

    def _load(self):
        url = _ZUNE_URL + self.tag
        return minidom.parse(urllib.urlopen(url))

    def __getattr__(self, name):

        # simple values
        if name in ['id', 'label', 'firstName', 'status', 'location', 'name', \
            'location', 'bio', 'totalPlays', 'userId']:
            return _getValue(self._node, name)

        # images
        if name in ['tileBig', 'tileSmall', 'backgroundLarge', 'backgroundSmall']:
            return _getImage(self._node, name)

        if name == 'badges':

            badges = []
            for badge in self._node.getElementsByTagName('badge'):
                badges.append(ZuneBadge(badge))
            return badges

        if name == 'following':

            following = []
            for artist in self._node.getElementsByTagName('followinfo'):
                following.append(ZuneArtist(artist.getElementsByTagName('artist')[0]))
            return following

        if name == 'favorites':
            favs = []
            for playlist in self._node.getElementsByTagName('playlist'):
                if playlist.getAttribute('type') == 'favs':
                    for track in playlist.getElementsByTagName('track'):
                        favs.append(ZuneTrack(track))
            return favs

        if name == 'recentSpins':
            recent = []
            for playlist in self._node.getElementsByTagName('playlist'):
                if playlist.getAttribute('type') == 'recent_spins':
                    for track in playlist.getElementsByTagName('track'):
                        recent.append(ZuneTrack(track))
            return recent

        if name == 'mostPlayed':
            mostPlayed = []
            for playlist in self._node.getElementsByTagName('playlist'):
                if playlist.getAttribute('type') == 'most_played':
                    for artist in playlist.getElementsByTagName('artist'):
                        mostPlayed.append(ZuneArtist(artist))
            return mostPlayed


class ZuneBadge:
    """
    Represents a zune badge, internal instantiation only

    Properties:
    - id
    - label
    - description
    - type
    - badgeImageSmall
    - badgeImageLarge
    - album ZuneAlbum
    - artist ZuneArtist
    """
    def __init__(self, node):
        self._node = node

    def __getattr__(self, name):

        # simple types
        if name in ['id', 'label', 'description', 'type']:
            return _getValue(self._node, name)

        if name in ['badgeImageSmall', 'badgeImageLarge']:
            return _getImage(self._node, name)

        if name == 'album':
            return ZuneAlbum(self._node.getElementsByTagName('album')[0])

        if name == 'artist':
            return ZuneArtist(self._node.getElementsByTagName('artist')[0])


class ZuneAlbum:
    """
    Represents an album, internal instantiation only

    Properties:
    - id
    - label
    - releaseTime
    - url
    - albumCoverSmall
    - albumCoverLarge
    - artist ZuneArtist
    """
    def __init__(self, node):
        self._node = node

    def __getattr__(self, name):

        if name in ['id', 'label', 'releaseTime']:
            return _getValue(self._node, name)

        # search child nodes due to descendant url nodes interfering
        if name == 'url':
            for node in self._node.childNodes:
                if node.nodeType == 1 and node.tagName == 'url':
                    return node.childNodes[0].nodeValue

        if name in ['albumCoverLarge', 'albumCoverSmall']:
            return _getImage(self._node, name)

        if name == 'artist':
            return _ZuneArtist(self._node.getElementsByTagName('artist')[0])


class ZuneArtist:
    """
    Represents an artist, internal instantiation only
    
    Properties:
    - id
    - label
    - url
    - artistImageLarge (not available in badge context)
    - artistImageSmall (not available in badge context)
    - totalPlays (mostPlayed context only)
    """
    def __init__(self, node):
        self._node = node

    def __getattr__(self, name):

        if name in ['id', 'label', 'url', 'totalPlays']:
            return _getValue(self._node, name)

        if name in ['artistImageLarge', 'artistImageSmall']:
            return _getImage(self._node, name)


class ZuneTrack:
    """
    Represents a song, internal instantiation only

    Properties:
    - id
    - label
    - genre
    - album ZuneAlbum
    """
    def __init__(self, node):
        self._node = node

    def __getattr__(self, name):

        if name in ['id', 'label', 'genre', 'buyURL', 'sendURL', 'setFavURL']:
            return _getValue(self._node, name)

        if name == 'album':
            return ZuneAlbum(self._node.getElementsByTagName('album')[0])


def _getValue(node, name):
    nodes = node.getElementsByTagName(name)
    if len(nodes) == 0:
        return None
    children = nodes[0].childNodes
    if len(children) == 0:
        return None
    return children[0].nodeValue

def _getImage(node, format):
    for image in node.getElementsByTagName('image'):
        if format == image.getAttribute('format'):
            return image.getElementsByTagName('url')[0].childNodes[0].nodeValue