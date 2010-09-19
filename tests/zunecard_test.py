import sys
import unittest
import urllib

from xml.dom import minidom
from os.path import join, dirname

sys.path.append( dirname(__file__) )

from zune import ZuneCard

def load_test_data(self):
    return minidom.parse(dirname(__file__) + '/test_data.xml')

class  ZuneCardTestCase(unittest.TestCase):


    def setUp(self):

        ZuneCard._load = load_test_data
        self.zuneCard = ZuneCard('NoogaGamer')


    def test_ZuneCard_returns_text_nodes(self):

        self.assertEqual(self.zuneCard.label, "NoogaGamer")
        self.assertEqual(self.zuneCard.status, "checking out the new Zune features")
        self.assertEqual(self.zuneCard.totalPlays, "39,367 plays")
        self.assertEqual(self.zuneCard.bio, "Father of two awesome boys, web developer, xbox gamer,\
 pontooner, barbecuer, wannabe guitarist, and more...")
        self.assertEqual(self.zuneCard.location, "Tennessee")

    
    def test_ZuneCard_returns_images(self):

        self.assertEqual(self.zuneCard.backgroundLarge, "http://cache-tiles.zune.net/tiles//hR/00/0\
HBpY3MvdTpYHlReRV9CUQ0BAwYAXQcFFABDQjAwL3VzZXJjYXJkYmFja2dyb3VuZC5hAAAAAAAAAP8bHbE=1b5d.jpg")
        self.assertEqual(self.zuneCard.backgroundSmall, "http://cache-tiles.zune.net/tiles//hR/00/0\
HBpY3MvdTpYHlReRV9CUQ0BAwYAXQcFFABDQjAwL3VzZXJjYXJkYmFja2dyb3VuZC5hAAAAAAAAAP8bHbE=1b5d.jpg")
        self.assertEqual(self.zuneCard.tileBig, "http://cache-tiles.zune.net/tiles//kp/aE/1HBpY3Mvd\
TpdHlNZQEJVWwcFTVRUGFZmZmUwNzAwL2dhbWVycGljLmQAAAAAAAAA+6uWuA==663e.jpg")
        self.assertEqual(self.zuneCard.tileSmall, "http://cache-tiles.zune.net/tiles//kp/aE/1HBpY3M\
vdTpdHlNZQEJVWwcFTVRUGFZmZmUwNzAwL2dhbWVycGljLmQAAAAAAAAA+6uWuA==663e.jpg")

    def test_ZuneCard_returns_badges(self):

        badges = self.zuneCard.badges
        self.assertEqual(len(self.zuneCard.badges), 93)

    def test_ZuneCard_badge_data(self):

        badge = self.zuneCard.badges[0]

        self.assertEqual(badge.id, '70840e44-459c-489c-abbf-0af9a89fafa6')
        self.assertEqual(badge.label, 'Bronze Album Power Listener')
        self.assertEqual(badge.description, '200 or more plays')
        self.assertEqual(badge.type, 'ActiveAlbumListener_Bronze')
        self.assertEqual(badge.badgeImageSmall, 'http://social.zune.net/xweb/lx/pic/minifeed/35x35-\
album-bronze.png')
        self.assertEqual(badge.badgeImageLarge, 'http://social.zune.net/xweb/lx/pic/minifeed/75x75-\
album-bronze.png')

        self.assertEqual(badge.album.id, '21570c02-0100-11db-89ca-0019b92a3933')
        self.assertEqual(badge.album.label, "Jason Mraz's Beautiful Mess: Live On Earth")
        self.assertEqual(badge.album.releaseTime, '2009')
        self.assertEqual(badge.album.url, "http://social.zune.net/album/Jason-Mraz/Jason-Mraz's-Bea\
utiful-Mess:-Live-On-Earth/21570c02-0100-11db-89ca-0019b92a3933/details")
        
        self.assertEqual(badge.album.albumCoverLarge, 'http://image.catalog.zune.net/v3.0/image/215\
70c02-0300-11db-89ca-0019b92a3933?resize=false&height=150')
        self.assertEqual(badge.album.albumCoverSmall, 'http://image.catalog.zune.net/v3.0/image/215\
70c02-0300-11db-89ca-0019b92a3933?resize=false&height=75')

        self.assertEqual(badge.artist.id, 'de490800-0600-11db-89ca-0019b92a3933')
        self.assertEqual(badge.artist.label, 'Jason Mraz')
        self.assertEqual(badge.artist.url, 'http://social.zune.net/artist/Jason-Mraz')


    def test_ZuneCard_following_data(self):

        following = self.zuneCard.following[0]

        self.assertEqual(following.id, '55240b00-0600-11db-89ca-0019b92a3933')
        self.assertEqual(following.label, 'Silversun Pickups')
        self.assertEqual(following.url, 'http://social.zune.net/artist/Silversun-Pickups')
        self.assertEqual(following.artistImageLarge, 'http://resources.zune.net/images/675fb187-4bd\
c-4070-bf33-f1e9fac9989b.PNG')
        self.assertEqual(following.artistImageSmall, 'http://resources.zune.net/images/90c53981-f35\
5-4872-902c-2f5b413b12fe.PNG')

    
    def test_ZuneCard_favorites_data(self):
        
        favorites = self.zuneCard.favorites
        self.assertEqual(len(favorites), 8)

        track = favorites[0]
        self.assertEqual(track.id, '3379da01-0100-11db-89ca-0019b92a3933')
        self.assertEqual(track.label, 'You Look Like I Need A Drink / Turn Those Clapping Hands Int\
o Angry Balled Fists')
        self.assertEqual(track.genre, 'rock')
        self.assertEqual(track.buyURL, 'http://social.zune.net/redirect?type=track&id=3379da01-0100\
-11db-89ca-0019b92a3933&target=web&action=buy&source=profile')
        self.assertEqual(track.sendURL, 'http://social.zune.net/my/sendmessage.aspx?AlbumName=The+O\
riginal+Cowboy&AlbumArtUrl=%2fxweb%2flx%2fpic%2fConstellation_75x75.jpg&mediaid=3379da01-0100-11db-\
89ca-0019b92a3933&type=Song&TrackName=You+Look+Like+I+Need+A+Drink+%2f+Turn+Those+Clapping+Hands+In\
to+Angry+Balled+Fists&ArtistName=Against+Me!&ru=%2fprofile')
        self.assertEqual(track.setFavURL, 'http://social.zune.net/profile/setfavorite.ashx?aid=3379\
da01-0100-11db-89ca-0019b92a3933&ru=http%3a%2f%2forigin-social.zune.net%2fzcard%2fusercardservi\
ce.ashx%3fzunetag%3dNoogaGamer')

        self.assertEqual(track.album.label, 'The Original Cowboy')
        self.assertEqual(track.album.releaseTime, '2009')

    def test_ZuneCard_recentSpins_data(self):

        favorites = self.zuneCard.recentSpins
        self.assertEqual(len(favorites), 8)

        track = favorites[0]
        self.assertEqual(track.id, '81138806-0100-11db-89ca-0019b92a3933')
        self.assertEqual(track.label, 'Poor Man Blues (Album Version)')
        self.assertEqual(track.buyURL, 'http://social.zune.net/redirect?type=track&id=81138806-\
0100-11db-89ca-0019b92a3933&target=web&action=buy&source=profile')
        self.assertEqual(track.sendURL, 'http://social.zune.net/my/sendmessage.aspx?AlbumName=The+G\
uitar+Song&AlbumArtUrl=%2fxweb%2flx%2fpic%2fConstellation_75x75.jpg&mediaid=81138806-0100-11db-89ca\
-0019b92a3933&type=Song&TrackName=Poor+Man+Blues+(Album+Version)&ArtistName=Jamey+Johnson&ru=%2fpro\
file')
        self.assertEqual(track.setFavURL, 'http://social.zune.net/profile/setfavorite.ashx?aid=8113\
8806-0100-11db-89ca-0019b92a3933&ru=http%3a%2f%2forigin-social.zune.net%2fzcard%2fusercardservice.a\
shx%3fzunetag%3dNoogaGamer')

        self.assertEqual(track.album.label, 'The Guitar Song')
        self.assertEqual(track.album.releaseTime, None)


    def test_ZuneCard_mostPlayed_data(self):

        mostPlayed = self.zuneCard.mostPlayed
        self.assertEqual(len(mostPlayed), 8)

        artist = mostPlayed[0]

        self.assertEqual(artist.label, 'Silversun Pickups')
        self.assertEqual(artist.totalPlays, '7,070,684 plays')

if __name__ == '__main__':
    unittest.main()

