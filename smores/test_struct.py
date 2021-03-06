# coding=utf8
import random

from twython import TwythonError
from twython import TwythonRateLimitError

__author__ = 'tony petrov'
# The fake object samples are taken from https://dev.twitter.com/rest/reference
from constants import *

fake_tweets = [
    {
        "coordinates": None,
        "favorited": False,
        "truncated": False,
        "created_at": "Wed Aug 29 17:12:58 +0000 2012",
        "id_str": "240859602684612608",
        "entities": {
            "urls": [
                {
                    "expanded_url": "/blog/twitter-certified-products",
                    "url": "https://t.co/MjJ8xAnT",
                    "indices": [
                        52,
                        73
                    ],
                    "display_url": "dev.twitter.com/blog/twitter-c\u2026"
                }
            ],
            "hashtags": [
                {'text': 'lala',
                 "indices": [
                     20,
                     34
                 ]
                 },
                {'text': 'gaga',
                 "indices": [
                     20,
                     34
                 ]
                 }
            ],
            "user_mentions": [

            ]
        },
        "in_reply_to_user_id_str": None,
        "contributors": None,
        "text": "Introducing the Twitter Certified Products Program: https://t.co/MjJ8xAnT",
        "retweet_count": 121,
        "in_reply_to_status_id_str": None,
        "id": 240859602684612608,
        "geo": None,
        "retweeted": False,
        "possibly_sensitive": False,
        "in_reply_to_user_id": None,
        "place": None,
        "user": {
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_sidebar_border_color": "C0DEED",
            "profile_background_tile": False,
            "name": "Twitter API",
            "profile_image_url": "http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
            "created_at": "Wed May 23 06:01:13 +0000 2007",
            "location": "San Francisco, CA",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": False,
            "id_str": "6253282",
            "entities": {
                "url": {
                    "urls": [
                        {
                            "expanded_url": None,
                            "url": "",
                            "indices": [
                                0,
                                22
                            ]
                        }
                    ]
                },
                "description": {
                    "urls": [

                    ]
                }
            },
            "default_profile": True,
            "contributors_enabled": True,
            "favourites_count": 24,
            "url": "",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
            "utc_offset": -28800,
            "id": 6253282,
            "profile_use_background_image": True,
            "listed_count": 10775,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 1212864,
            "protected": False,
            "notifications": None,
            "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
            "profile_background_color": "C0DEED",
            "verified": True,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "The Real Twitter API. I tweet about API changes, service issues and happily answer questions about Twitter and our API. Don't get an answer? It's on my website.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
            "statuses_count": 3333,
            "friends_count": 31,
            "following": None,
            "show_all_inline_media": False,
            "screen_name": "twitterapi"
        },
        "in_reply_to_screen_name": None,
        "source": "YoruFukurou",
        "in_reply_to_status_id": None
    },
    {
        "coordinates": None,
        "favorited": False,
        "truncated": False,
        "created_at": "Sat Aug 25 17:26:51 +0000 2012",
        "id_str": "239413543487819778",
        "entities": {
            "urls": [
                {
                    "expanded_url": "/issues/485",
                    "url": "https://t.co/p5bOzH0k",
                    "indices": [
                        97,
                        118
                    ],
                    "display_url": "dev.twitter.com/issues/485"
                }
            ],
            "hashtags": [
                {'text': 'dada',
                 "indices": [
                     20,
                     34
                 ]
                 },
                {'text': 'gaga',
                 "indices": [
                     20,
                     34
                 ]
                 }
            ],
            "user_mentions": [

            ]
        },
        "in_reply_to_user_id_str": None,
        "contributors": None,
        "text": "We are working to resolve issues with application management & logging in to the dev portal: https://t.co/p5bOzH0k ^TS",
        "retweet_count": 105,
        "in_reply_to_status_id_str": None,
        "id": 239413543487819778,
        "geo": None,
        "retweeted": False,
        "possibly_sensitive": False,
        "in_reply_to_user_id": None,
        "place": None,
        "user": {
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_sidebar_border_color": "C0DEED",
            "profile_background_tile": False,
            "name": "Twitter API",
            "profile_image_url": "http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
            "created_at": "Wed May 23 06:01:13 +0000 2007",
            "location": "San Francisco, CA",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": False,
            "id_str": "6253282",
            "entities": {
                "url": {
                    "urls": [
                        {
                            "expanded_url": None,
                            "url": "",
                            "indices": [
                                0,
                                22
                            ]
                        }
                    ]
                },
                "description": {
                    "urls": [

                    ]
                }
            },
            "default_profile": True,
            "contributors_enabled": True,
            "favourites_count": 24,
            "url": "",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
            "utc_offset": -28800,
            "id": 6253282,
            "profile_use_background_image": True,
            "listed_count": 10775,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 1212864,
            "protected": False,
            "notifications": None,
            "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
            "profile_background_color": "C0DEED",
            "verified": True,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "The Real Twitter API. I tweet about API changes, service issues and happily answer questions about Twitter and our API. Don't get an answer? It's on my website.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
            "statuses_count": 3333,
            "friends_count": 31,
            "following": None,
            "show_all_inline_media": False,
            "screen_name": "twitterapi"
        },
        "in_reply_to_screen_name": None,
        "source": "YoruFukurou",
        "in_reply_to_status_id": None
    }
]
broken_tweets = [
    {
        "coordinates": None,
        "favorited": False,
        "truncated": False,
        "created_at": "Wed Aug 29 17:12:58 +0000 2096",
        "id_str": "240859602684612608",
        "entities": {
            "urls": [
                {
                    "expanded_url": "/blog/twitter-certified-products",
                    "url": "https://t.co/MjJ8xAnT",
                    "indices": [
                        52,
                        73
                    ],
                    "display_url": "dev.twitter.com/blog/twitter-c\u2026"
                }
            ],
            "hashtags": [
                {'text': u'ðå¶³¤éåäú¡²³½¼¾',
                 "indices": [
                     20,
                     34
                 ]
                 },
                {'text': 'gaga',
                 "indices": [
                     20,
                     34
                 ]
                 }
            ],
            "user_mentions": [

            ]
        },
        "in_reply_to_user_id_str": None,
        "contributors": None,
        "text": u"Intröducing the Twitter Certified Products Program: https://t.co/MjJ8xAnT n¶áäöëç",
        "retweet_count": 121,
        "in_reply_to_status_id_str": None,
        "id": 240859602684612608,
        "geo": None,
        "retweeted": False,
        "possibly_sensitive": False,
        "in_reply_to_user_id": None,
        "place": None,
        "user": {
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_sidebar_border_color": "C0DEED",
            "profile_background_tile": False,
            "name": u"Twitter APï",
            "profile_image_url": "http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
            "created_at": "Wed May 23 06:01:13 +0000 2007",
            "location": u"San Francisco, CÄ",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": False,
            "id_str": "6253282",
            "entities": {
                "url": {
                    "urls": [
                        {
                            "expanded_url": None,
                            "url": "",
                            "indices": [
                                0,
                                22
                            ]
                        }
                    ]
                },
                "description": {
                    "urls": [

                    ]
                }
            },
            "default_profile": True,
            "contributors_enabled": True,
            "favourites_count": 24,
            "url": "",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
            "utc_offset": -28800,
            "id": 6253282,
            "profile_use_background_image": True,
            "listed_count": 10775,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 1212864,
            "protected": False,
            "notifications": None,
            "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
            "profile_background_color": "C0DEED",
            "verified": True,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "The Real Twitter API. I tweet about API changes, service issues and happily answer questions about Twitter and our API. Don't get an answer? It's on my website.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
            "statuses_count": 3333,
            "friends_count": 31,
            "following": None,
            "show_all_inline_media": False,
            "screen_name": "twitterapi"
        },
        "in_reply_to_screen_name": None,
        "source": "YoruFukurou",
        "in_reply_to_status_id": None
    },{
        "coordinates": None,
        "favorited": False,
        "truncated": False,
        "created_at": "Wed Aug 29 17:12:58 +0000 1996",
        "id_str": "240859602684612608",
        "entities": {
            "urls": [
                {
                    "expanded_url": "/blog/twitter-certified-products",
                    "url": "https://t.co/MjJ8xAnT",
                    "indices": [
                        52,
                        73
                    ],
                    "display_url": "dev.twitter.com/blog/twitter-c\u2026"
                }
            ],
            "hashtags": [
                {'text': u'ðå¶³¤éåäú¡²³½¼¾',
                 "indices": [
                     20,
                     34
                 ]
                 },
                {'text': 'gaga',
                 "indices": [
                     20,
                     34
                 ]
                 }
            ],
            "user_mentions": [

            ]
        },
        "in_reply_to_user_id_str": None,
        "contributors": None,
        "text": u"Intröducing \u0420\u043e\u0441\u0441\u0438\u044f n¶áäöëç \u02ff\u0333",
        "retweet_count": 121,
        "in_reply_to_status_id_str": None,
        "id": 240859626612608,
        "geo": None,
        "retweeted": False,
        "possibly_sensitive": False,
        "in_reply_to_user_id": None,
        "place": None,
        "in_reply_to_screen_name": None,
        "source": "YoruFukurou",
        "in_reply_to_status_id": None
    },    {
        "coordinates": None,
        "favorited": False,
        "truncated": False,
        "created_at": "Wed Aug 29 17:12:58 +0000 2006",
        "id_str": "240859602684612608",
        "entities": {
            "urls": [
                {
                    "expanded_url": "/blog/twitter-certified-products",
                    "url": "https://t.co/MjJ8xAnT",
                    "indices": [
                        52,
                        73
                    ],
                    "display_url": "dev.twitter.com/blog/twitter-c\u2026"
                }
            ],
            "hashtags": [
                {'text': u'ðå¶³¤éåäú¡²³½¼¾',
                 "indices": [
                     20,
                     34
                 ]
                 },
                {'text': 'gaga',
                 "indices": [
                     20,
                     34
                 ]
                 }
            ],
            "user_mentions": [

            ]
        },
        "in_reply_to_user_id_str": None,
        "contributors": None,
        "text": u"Intröducing the Twitter Certified Products Program: https://t.co/MjJ8xAnT n¶áäöëç",
        "retweet_count": 121,
        "in_reply_to_status_id_str": None,
        "id": 240859602684612608,
        "geo": None,
        "retweeted": False,
        "possibly_sensitive": False,
        "in_reply_to_user_id": None,
        "place": None,
        "user": {
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_sidebar_border_color": "C0DEED",
            "profile_background_tile": False,
            "name": u"Twitter APï",
            "profile_image_url": "http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
            "created_at": "Wed May 23 06:01:13 +0000 2007",
            "location": u"San Francisco, CÄ",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": False,
            "default_profile": True,
            "contributors_enabled": True,
            "favourites_count": 24,
            "url": "",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
            "utc_offset": -28800,
            "profile_use_background_image": True,
            "listed_count": 10775,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": -5,
            "protected": False,
            "notifications": None,
            "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
            "profile_background_color": "C0DEED",
            "verified": True,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": u"\u0555\u0456\u05ab\u02bb",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
            "statuses_count": 3333,
            "friends_count": None,
            "following": None,
            "show_all_inline_media": False,
            "screen_name": "twitterapi"
        },
        "in_reply_to_screen_name": None,
        "source": "YoruFukurou",
        "in_reply_to_status_id": None
    }]
fr_list = {
    "previous_cursor": 0,
    "previous_cursor_str": "0",
    "next_cursor": 1333504313713126852,
    "users": [
        {
            "profile_sidebar_fill_color": "252429",
            "profile_sidebar_border_color": "181A1E",
            "profile_background_tile": False,
            "name": "Sylvain Carle",
            "profile_image_url": "http://a0.twimg.com/profile_images/2838630046/4b82e286a659fae310012520f4f756bb_normal.png",
            "created_at": "Thu Jan 18 00:10:45 +0000 2007",
            "location": "San Francisco",
            "follow_request_sent": False,
            "profile_link_color": "2FC2EF",
            "is_translator": False,
            "id_str": "657693",
            "default_profile": False,
            "contributors_enabled": True,
            "favourites_count": 1973,
            "url": "http://afroginthevalley.com/",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/657693/1353537845",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2838630046/4b82e286a659fae310012520f4f756bb_normal.png",
            "utc_offset": -18000,
            "id": 657693,
            "profile_use_background_image": True,
            "listed_count": 324,
            "profile_text_color": "666666",
            "lang": "en",
            "followers_count": 4993,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme9/bg.gif",
            "profile_background_color": "1A1B1F",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Eastern Time (US & Canada)",
            "description": "Developer Advocate at Twitter.\r\n\r\nInternet, opensource, media & geo/local geek.\r\n\r\nFollow @sylvain for LANG=FR.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/images/themes/theme9/bg.gif",
            "statuses_count": 8504,
            "friends_count": 2743,
            "following": True,
            "screen_name": "froginthevalley"
        },
        {
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_sidebar_border_color": "C0DEED",
            "profile_background_tile": True,
            "name": "Site Streams Beta",
            "profile_image_url": "http://a0.twimg.com/profile_images/2284174702/1tyzesnfmqhqsl4xuf5a_normal.png",
            "created_at": "Fri Aug 27 18:04:38 +0000 2010",
            "location": "San Francisco, CA",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": False,
            "id_str": "183709371",
            "default_profile": False,
            "contributors_enabled": True,
            "favourites_count": 0,
            "url": "http://twitter.com",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/183709371/1347395034",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2284174702/1tyzesnfmqhqsl4xuf5a_normal.png",
            "utc_offset": None,
            "id": 183709371,
            "profile_use_background_image": True,
            "listed_count": 195,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 9732,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/656938621/vvhperynuny1q6em9i7k.png",
            "profile_background_color": "C0DEED",
            "verified": True,
            "geo_enabled": False,
            "time_zone": None,
            "description": "This account is no longer in use.  Please see @twitterapi for announcements about the Sitestreams API.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/656938621/vvhperynuny1q6em9i7k.png",
            "statuses_count": 178,
            "friends_count": 5,
            "following": True,
            "screen_name": "sitestreams"
        },
        {
            "profile_sidebar_fill_color": "C7E0FF",
            "profile_sidebar_border_color": "FFFFFF",
            "profile_background_tile": True,
            "name": "Arne Roomann-Kurrik",
            "profile_image_url": "http://a0.twimg.com/profile_images/24229162/arne001_normal.jpg",
            "created_at": "Thu Jul 19 15:58:07 +0000 2007",
            "location": "Scan Francesco",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": False,
            "id_str": "7588892",
            "default_profile": False,
            "contributors_enabled": False,
            "favourites_count": 798,
            "url": "http://start.roomanna.com",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/7588892/1347312754",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/24229162/arne001_normal.jpg",
            "utc_offset": -28800,
            "id": 7588892,
            "profile_use_background_image": True,
            "listed_count": 172,
            "profile_text_color": "000000",
            "lang": "en",
            "followers_count": 3876,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/342542280/background7.png",
            "profile_background_color": "8FC1FF",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "Developer Advocate at Twitter, practitioner of dark sandwich arts. ",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/342542280/background7.png",
            "statuses_count": 3245,
            "friends_count": 589,
            "following": True,
            "screen_name": "kurrik"
        },
        {
            "profile_sidebar_fill_color": "252429",
            "profile_sidebar_border_color": "FFFFFF",
            "profile_background_tile": True,
            "name": "Sean Cook",
            "profile_image_url": "http://a0.twimg.com/profile_images/2757776645/23872cfcee4dc7279facb8fb0a6cb559_normal.png",
            "created_at": "Sat May 09 17:58:22 +0000 2009",
            "location": "San Francisco",
            "follow_request_sent": False,
            "profile_link_color": "2FC2EF",
            "is_translator": False,
            "id_str": "38895958",
            "default_profile": False,
            "contributors_enabled": True,
            "favourites_count": 698,
            "url": None,
            "profile_banner_url": "https://si0.twimg.com/profile_banners/38895958/1346803787",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2757776645/23872cfcee4dc7279facb8fb0a6cb559_normal.png",
            "utc_offset": -28800,
            "id": 38895958,
            "profile_use_background_image": False,
            "listed_count": 198,
            "profile_text_color": "666666",
            "lang": "en",
            "followers_count": 11191,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/495742332/purty_wood.png",
            "profile_background_color": "42454B",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "I taught your phone that thing you like.  The Mobile Partner Engineer @Twitter. ",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/495742332/purty_wood.png",
            "statuses_count": 2909,
            "friends_count": 1217,
            "following": True,
            "screen_name": "theSeanCook"
        },
        {
            "profile_sidebar_fill_color": "C0DFEC",
            "profile_sidebar_border_color": "FFFFFF",
            "profile_background_tile": True,
            "name": "Ian Chan",
            "profile_image_url": "http://a0.twimg.com/profile_images/2467844172/image_normal.jpg",
            "created_at": "Thu Mar 05 06:42:32 +0000 2009",
            "location": "Toronto  San Francisco",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": True,
            "id_str": "22891211",
            "default_profile": False,
            "contributors_enabled": True,
            "favourites_count": 3267,
            "url": "http://chanian.com",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/22891211/1348559711",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2467844172/image_normal.jpg",
            "utc_offset": -18000,
            "id": 22891211,
            "profile_use_background_image": True,
            "listed_count": 186,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 7356,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/663303208/kpzmxbnwvxk9cfr7hpdw.png",
            "profile_background_color": "022330",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Eastern Time (US & Canada)",
            "description": "Canadian, UofT Alumn, Platform Engineer for @twitter, poker player.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/663303208/kpzmxbnwvxk9cfr7hpdw.png",
            "statuses_count": 6892,
            "friends_count": 622,
            "following": True,
            "screen_name": "chanian"
        },
        {
            "profile_sidebar_fill_color": "000B17",
            "profile_sidebar_border_color": "F7B565",
            "profile_background_tile": False,
            "name": "akashgarg",
            "profile_image_url": "http://a0.twimg.com/profile_images/1800189528/image1328232461_normal.png",
            "created_at": "Fri Sep 21 18:23:07 +0000 2007",
            "location": "San Francisco",
            "follow_request_sent": False,
            "profile_link_color": "448668",
            "is_translator": False,
            "id_str": "9019482",
            "default_profile": False,
            "contributors_enabled": False,
            "favourites_count": 57,
            "url": "http://www.linkedin.com/in/akashdgarg",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/9019482/1348061531",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/1800189528/image1328232461_normal.png",
            "utc_offset": -28800,
            "id": 9019482,
            "profile_use_background_image": False,
            "listed_count": 120,
            "profile_text_color": "004358",
            "lang": "en",
            "followers_count": 2649,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/378356748/x56a919dd9dbd34581a3f162af04a4e8.jpg",
            "profile_background_color": "001329",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "Director of Engineering, Growth Team @ Twitter",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/378356748/x56a919dd9dbd34581a3f162af04a4e8.jpg",
            "statuses_count": 462,
            "friends_count": 1445,
            "following": True,
            "screen_name": "akashgarg"
        },
        {
            "profile_sidebar_fill_color": "C0DFEC",
            "profile_sidebar_border_color": "A8C7F7",
            "profile_background_tile": False,
            "name": "Ben Ward",
            "profile_image_url": "http://a0.twimg.com/profile_images/1409204408/2011_normal.png",
            "created_at": "Mon Nov 13 13:39:24 +0000 2006",
            "location": "San Francisco, CA",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": True,
            "id_str": "12249",
            "default_profile": False,
            "contributors_enabled": False,
            "favourites_count": 16749,
            "url": "http://benward.me",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/12249/1348598804",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/1409204408/2011_normal.png",
            "utc_offset": -28800,
            "id": 12249,
            "profile_use_background_image": True,
            "listed_count": 388,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 7982,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/637103983/474kwsozag6mi0hkvwmo.jpeg",
            "profile_background_color": "022330",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "Frontend software engineer at @twitter, purveyor of shitty puns everywhere, @benwwward and @thepastrybox writer, @microformats community admin. Bit of a whiner.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/637103983/474kwsozag6mi0hkvwmo.jpeg",
            "statuses_count": 15542,
            "friends_count": 588,
            "following": True,
            "screen_name": "BenWard"
        },
        {
            "profile_sidebar_fill_color": "F0F0F0",
            "profile_sidebar_border_color": "000000",
            "profile_background_tile": False,
            "name": "Kenneth P Kufluk",
            "profile_image_url": "http://a0.twimg.com/profile_images/2734520194/9e5843b95abce47b7056b17ce7bbc18f_normal.png",
            "created_at": "Thu Mar 05 13:05:04 +0000 2009",
            "location": "San Francisco, California",
            "follow_request_sent": False,
            "profile_link_color": "333333",
            "is_translator": False,
            "id_str": "22915745",
            "default_profile": False,
            "contributors_enabled": False,
            "favourites_count": 1280,
            "url": "http://kenneth.kufluk.com",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/22915745/1353469520",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2734520194/9e5843b95abce47b7056b17ce7bbc18f_normal.png",
            "utc_offset": -28800,
            "id": 22915745,
            "profile_use_background_image": True,
            "listed_count": 62,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 3925,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/173989056/silly_twitter_bg.jpg",
            "profile_background_color": "161712",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "The neth is essential.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/173989056/silly_twitter_bg.jpg",
            "statuses_count": 10009,
            "friends_count": 222,
            "following": True,
            "screen_name": "kpk"
        },
        {
            "profile_sidebar_fill_color": "F6F6F6",
            "profile_sidebar_border_color": "FFFFFF",
            "profile_background_tile": False,
            "name": "Seth Bindernagel",
            "profile_image_url": "http://a0.twimg.com/profile_images/2867434205/c5bf4196b723e7d0494bd4b5ccf79346_normal.jpeg",
            "created_at": "Thu Mar 15 21:49:02 +0000 2007",
            "location": "San Francisco, CA",
            "follow_request_sent": False,
            "profile_link_color": "FF3300",
            "is_translator": False,
            "id_str": "1249881",
            "default_profile": False,
            "contributors_enabled": True,
            "favourites_count": 278,
            "url": None,
            "profile_banner_url": "https://si0.twimg.com/profile_banners/1249881/1348078082",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2867434205/c5bf4196b723e7d0494bd4b5ccf79346_normal.jpeg",
            "utc_offset": -28800,
            "id": 1249881,
            "profile_use_background_image": True,
            "listed_count": 82,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 3341,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/698916047/dcd323b0502e46e4d3a337caf8694aef.jpeg",
            "profile_background_color": "709397",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "I work for Twitter and I love Cleveland Sports. https://about.me/binder",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/698916047/dcd323b0502e46e4d3a337caf8694aef.jpeg",
            "statuses_count": 1863,
            "friends_count": 690,
            "following": True,
            "screen_name": "binder"
        },
        {
            "profile_sidebar_fill_color": "A0C5C7",
            "profile_sidebar_border_color": "86A4A6",
            "profile_background_tile": False,
            "name": "Jason Costa",
            "profile_image_url": "http://a0.twimg.com/profile_images/1751674923/new_york_beard_normal.jpg",
            "created_at": "Wed May 28 00:20:15 +0000 2008",
            "location": "",
            "follow_request_sent": False,
            "profile_link_color": "FF3300",
            "is_translator": True,
            "id_str": "14927800",
            "default_profile": False,
            "contributors_enabled": False,
            "favourites_count": 1053,
            "url": "http://www.jason-costa.blogspot.com/",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/1751674923/new_york_beard_normal.jpg",
            "utc_offset": -28800,
            "id": 14927800,
            "profile_use_background_image": True,
            "listed_count": 161,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 11874,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme6/bg.gif",
            "profile_background_color": "709397",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "Platform at Twitter",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/images/themes/theme6/bg.gif",
            "statuses_count": 5745,
            "friends_count": 175,
            "following": True,
            "screen_name": "jasoncosta"
        },
        {
            "profile_sidebar_fill_color": "FEFEFE",
            "profile_sidebar_border_color": "000000",
            "profile_background_tile": True,
            "name": "Connor Sears",
            "profile_image_url": "http://a0.twimg.com/profile_images/2659620048/aca7116831caaeb410b8b98be63c8874_normal.jpeg",
            "created_at": "Mon Mar 19 16:19:32 +0000 2007",
            "location": "Palo Alto",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": False,
            "id_str": "1523501",
            "default_profile": False,
            "contributors_enabled": False,
            "favourites_count": 2716,
            "url": "http://connorsears.com",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/1523501/1351629702",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2659620048/aca7116831caaeb410b8b98be63c8874_normal.jpeg",
            "utc_offset": -28800,
            "id": 1523501,
            "profile_use_background_image": True,
            "listed_count": 81,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 3055,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/698065178/00ca3a67587ddb2792d9b05a45cf42b1.jpeg",
            "profile_background_color": "262626",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "Co-creator of Ratchet (@GoRatchet). Product Designer formerly at Twitter. I bless the rains down in Africa.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/698065178/00ca3a67587ddb2792d9b05a45cf42b1.jpeg",
            "statuses_count": 3992,
            "friends_count": 195,
            "following": True,
            "screen_name": "connors"
        },
        {
            "profile_sidebar_fill_color": "C5DAE9",
            "profile_sidebar_border_color": "777777",
            "profile_background_tile": False,
            "name": "Arnaud Meunier",
            "profile_image_url": "http://a0.twimg.com/profile_images/1374353291/image_normal.jpg",
            "created_at": "Mon Mar 02 22:53:50 +0000 2009",
            "location": "San Francisco, CA",
            "follow_request_sent": False,
            "profile_link_color": "21759B",
            "is_translator": True,
            "id_str": "22548447",
            "default_profile": False,
            "contributors_enabled": False,
            "favourites_count": 108,
            "url": "http://twitoaster.com",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/22548447/1348188118",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/1374353291/image_normal.jpg",
            "utc_offset": -28800,
            "id": 22548447,
            "profile_use_background_image": False,
            "listed_count": 944,
            "profile_text_color": "555555",
            "lang": "en",
            "followers_count": 22315,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/107336160/twitter-background-twitoaster.png",
            "profile_background_color": "E4ECF0",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "French expat. Eng manager at Twitter.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/107336160/twitter-background-twitoaster.png",
            "statuses_count": 1926,
            "friends_count": 325,
            "following": True,
            "screen_name": "rno"
        },
        {
            "profile_sidebar_fill_color": "DAECF4",
            "profile_sidebar_border_color": "C6E2EE",
            "profile_background_tile": True,
            "name": "Jeremy Cloud",
            "profile_image_url": "http://a0.twimg.com/profile_images/2785231602/3697a603c0a067328d87beb15d2b59f0_normal.jpeg",
            "created_at": "Mon Jun 09 17:00:58 +0000 2008",
            "location": "Somerville, MA",
            "follow_request_sent": False,
            "profile_link_color": "1F98C7",
            "is_translator": False,
            "id_str": "15062340",
            "default_profile": False,
            "contributors_enabled": False,
            "favourites_count": 123,
            "url": "http://about.me/jeremy.cloud",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/15062340/1351613822",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2785231602/3697a603c0a067328d87beb15d2b59f0_normal.jpeg",
            "utc_offset": -18000,
            "id": 15062340,
            "profile_use_background_image": True,
            "listed_count": 96,
            "profile_text_color": "663B12",
            "lang": "en",
            "followers_count": 3494,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/480149151/NSTexturedFullScreenBackgroundColor.png",
            "profile_background_color": "C6E2EE",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Eastern Time (US & Canada)",
            "description": "Former snake charmer.  Engineer at Twitter.  Father of @baby_cloud.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/480149151/NSTexturedFullScreenBackgroundColor.png",
            "statuses_count": 1514,
            "friends_count": 302,
            "following": True,
            "screen_name": "jeremycloud"
        },
        {
            "profile_sidebar_fill_color": "F6FFD1",
            "profile_sidebar_border_color": "FFFFFF",
            "profile_background_tile": True,
            "name": "Glen D Sanford",
            "profile_image_url": "http://a0.twimg.com/profile_images/917780110/0629072227-00_normal.jpg",
            "created_at": "Wed Apr 14 20:59:58 +0000 2010",
            "location": "Alameda, CA",
            "follow_request_sent": False,
            "profile_link_color": "009999",
            "is_translator": False,
            "id_str": "133031077",
            "default_profile": False,
            "contributors_enabled": False,
            "favourites_count": 38,
            "url": "http://glen.nu",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/133031077/1351918195",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/917780110/0629072227-00_normal.jpg",
            "utc_offset": -28800,
            "id": 133031077,
            "profile_use_background_image": True,
            "listed_count": 56,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 2680,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/658791112/hxelotrdy3h7qga87mv1.jpeg",
            "profile_background_color": "131516",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "Software Engineering Manager for @twittereng, fundamentally ok guy",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/658791112/hxelotrdy3h7qga87mv1.jpeg",
            "statuses_count": 1516,
            "friends_count": 147,
            "following": True,
            "screen_name": "9len"
        },
        {
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_sidebar_border_color": "C0DEED",
            "profile_background_tile": True,
            "name": "Support",
            "profile_image_url": "http://a0.twimg.com/profile_images/2320882833/2whv6cuhvbal751uss8u_normal.png",
            "created_at": "Thu Dec 04 18:51:57 +0000 2008",
            "location": "Twitter HQ",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": False,
            "id_str": "17874544",
            "default_profile": False,
            "contributors_enabled": True,
            "favourites_count": 45,
            "url": "http://support.twitter.com",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/17874544/1347394418",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2320882833/2whv6cuhvbal751uss8u_normal.png",
            "utc_offset": -32400,
            "id": 17874544,
            "profile_use_background_image": True,
            "listed_count": 11116,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 1901267,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/656929496/y6jd4l68p18hrm52f0ez.png",
            "profile_background_color": "C0DEED",
            "verified": True,
            "geo_enabled": True,
            "time_zone": "Alaska",
            "description": "Updates from Twitter User Support. We're unable to assist with account suspension/verification.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/656929496/y6jd4l68p18hrm52f0ez.png",
            "statuses_count": 2154,
            "friends_count": 30,
            "following": True,
            "screen_name": "Support"
        },
        {
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_sidebar_border_color": "C0DEED",
            "profile_background_tile": False,
            "name": "Matt Harris",
            "profile_image_url": "http://a0.twimg.com/profile_images/554181350/matt_normal.jpg",
            "created_at": "Sat Feb 17 20:49:54 +0000 2007",
            "location": "SFO/LHR/YVR/JAX/IAD",
            "follow_request_sent": False,
            "profile_link_color": "0084B4",
            "is_translator": False,
            "id_str": "777925",
            "default_profile": True,
            "contributors_enabled": True,
            "favourites_count": 235,
            "url": "http://www.themattharris.com",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/777925/1351367661",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/554181350/matt_normal.jpg",
            "utc_offset": -28800,
            "id": 777925,
            "profile_use_background_image": True,
            "listed_count": 304,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 8208,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
            "profile_background_color": "C0DEED",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "Maybe the Nick Fury of @twitter. Married to @cindyli. Kryptonite hurts me.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
            "statuses_count": 4551,
            "friends_count": 433,
            "following": True,
            "screen_name": "themattharris"
        },
        {
            "profile_sidebar_fill_color": "A0C5C7",
            "profile_sidebar_border_color": "FFFFFF",
            "profile_background_tile": False,
            "name": "April Underwood",
            "profile_image_url": "http://a0.twimg.com/profile_images/2623063815/image_normal.jpg",
            "created_at": "Thu Apr 12 00:11:07 +0000 2007",
            "location": "San Francisco, CA",
            "follow_request_sent": False,
            "profile_link_color": "14A395",
            "is_translator": False,
            "id_str": "4265731",
            "default_profile": False,
            "contributors_enabled": True,
            "favourites_count": 3024,
            "url": "http://www.aprilunderwood.com",
            "profile_banner_url": "https://si0.twimg.com/profile_banners/4265731/1352050638",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2623063815/image_normal.jpg",
            "utc_offset": -28800,
            "id": 4265731,
            "profile_use_background_image": False,
            "listed_count": 348,
            "profile_text_color": "333333",
            "lang": "en",
            "followers_count": 16976,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/662816188/cbyxvatdol1hg8r7c1qb.jpeg",
            "profile_background_color": "F4F5B1",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "You can't drink from a martini glass while sitting in a rocking chair. I work at @Twitter.",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/662816188/cbyxvatdol1hg8r7c1qb.jpeg",
            "statuses_count": 8452,
            "friends_count": 1328,
            "following": True,
            "screen_name": "aunder"
        },
        {
            "profile_sidebar_fill_color": "121212",
            "profile_sidebar_border_color": "000000",
            "profile_background_tile": False,
            "name": "Kelton Lynn",
            "profile_image_url": "http://a0.twimg.com/profile_images/384067053/n209356_35266280_356207_2_normal.jpg",
            "created_at": "Mon Mar 30 16:30:42 +0000 2009",
            "location": "San Francisco",
            "follow_request_sent": False,
            "profile_link_color": "999999",
            "is_translator": False,
            "id_str": "27674040",
            "default_profile": False,
            "contributors_enabled": True,
            "favourites_count": 421,
            "url": None,
            "profile_banner_url": "https://si0.twimg.com/profile_banners/27674040/1348163748",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/384067053/n209356_35266280_356207_2_normal.jpg",
            "utc_offset": -28800,
            "id": 27674040,
            "profile_use_background_image": True,
            "listed_count": 174,
            "profile_text_color": "505050",
            "lang": "en",
            "followers_count": 10971,
            "protected": False,
            "notifications": False,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/424627076/aged_planks_843_10949.jpg",
            "profile_background_color": "000000",
            "verified": False,
            "geo_enabled": True,
            "time_zone": "Pacific Time (US & Canada)",
            "description": "Mobile BizDev at Twitter, former Boulderite, bleed Cardinal, SF transplant, love athletics/competition, consumer tech, entrepreneurship, family/friends...life",
            "default_profile_image": False,
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/424627076/aged_planks_843_10949.jpg",
            "statuses_count": 3166,
            "friends_count": 1216,
            "following": True,
            "screen_name": "keltonlynn"
        }
    ],
    "next_cursor_str": "1333504313713126852"
}
fake_list = {
    "created_at": "Fri Nov 04 21:22:36 +0000 2011",
    "slug": "goonies",
    "name": "Goonies",
    "full_name": "@kurrik\/goonies",
    "description": "For life",
    "mode": "public",
    "following": False,
    "user": {
        "geo_enabled": True,
        "profile_background_image_url_https": "https:\/\/si0.twimg.com\/profile_background_images\/342542280\/background7.png",
        "profile_background_color": "8fc1ff",
        "protected": False,
        "default_profile": False,
        "listed_count": 127,
        "profile_background_tile": True,
        "created_at": "Thu Jul 19 15:58:07 +0000 2007",
        "friends_count": 291,
        "name": "Arne Roomann-Kurrik",
        "profile_sidebar_fill_color": "c7e0ff",
        "notifications": False,
        "utc_offset": -28800,
        "profile_image_url_https": "https:\/\/si0.twimg.com\/profile_images\/24229162\/arne001_normal.jpg",
        "description": "Developer Advocate at Twitter, practitioner of dark sandwich arts. ",
        "display_url": "roomanna.com",
        "following": False,
        "verified": False,
        "favourites_count": 190,
        "profile_sidebar_border_color": "6baeff",
        "followers_count": 1705,
        "profile_image_url": "http:\/\/a2.twimg.com\/profile_images\/24229162\/arne001_normal.jpg",
        "default_profile_image": False,
        "contributors_enabled": False,
        "deactivated_bit": False,
        "statuses_count": 1935,
        "profile_use_background_image": True,
        "location": "Scan Francesco",
        "id_str": "7588892",
        "show_all_inline_media": False,
        "profile_text_color": "000000",
        "screen_name": "kurrik",
        "follow_request_sent": False,
        "profile_background_image_url": "http:\/\/a2.twimg.com\/profile_background_images\/342542280\/background7.png",
        "url": "http:\/\/t.co\/SSiVavc4",
        "expanded_url": "http:\/\/roomanna.com",
        "is_translator": False,
        "time_zone": "Pacific Time (US & Canada)",
        "profile_link_color": "0084B4",
        "id": 7588892,
        "entities": {
            "urls": [

            ],
            "user_mentions": [

            ],
            "hashtags": [

            ]
        },
        "suspended": False,
        "lang": "en"
    },
    "member_count": 0,
    "id_str": "58300198",
    "subscriber_count": 0,
    "id": 58300198,
    "uri": "\/kurrik\/goonies"
}
fake_lookup_data = [
    {
        "name": "Twitter API",
        "profile_sidebar_fill_color": "DDEEF6",
        "profile_background_tile": False,
        "profile_sidebar_border_color": "C0DEED",
        "profile_image_url": "http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
        "location": "San Francisco, CA",
        "created_at": "Wed May 23 06:01:13 +0000 2007",
        "follow_request_sent": False,
        "id_str": "6253282",
        "profile_link_color": "0084B4",
        "is_translator": False,
        "default_profile": True,
        "favourites_count": 24,
        "contributors_enabled": True,
        "url": "",
        "profile_image_url_https": "https://si0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png",
        "utc_offset": -28800,
        "id": 6253282,
        "profile_use_background_image": True,
        "listed_count": 10713,
        "profile_text_color": "333333",
        "lang": "en",
        "followers_count": 1198334,
        "protected": False,
        "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
        "geo_enabled": True,
        "description": "The Real Twitter API. I tweet about API changes, service issues and happily answer questions about Twitter and our API. Don't get an answer? It's on my website.",
        "profile_background_color": "C0DEED",
        "verified": True,
        "notifications": False,
        "time_zone": "Pacific Time (US & Canada)",
        "statuses_count": 3331,
        "status": {
            "coordinates": None,
            "created_at": "Fri Aug 24 16:15:49 +0000 2012",
            "favorited": False,
            "truncated": False,
            "id_str": "239033279343382529",
            "in_reply_to_user_id_str": "134727529",
            "text": "@gregclermont no, there is not. ^TS",
            "contributors": None,
            "retweet_count": 0,
            "id": 239033279343382529,
            "in_reply_to_status_id_str": "238933943146131456",
            "geo": None,
            "retweeted": False,
            "in_reply_to_user_id": 134727529,
            "place": None,
            "source": "YoruFukurou",
            "in_reply_to_screen_name": "gregclermont",
            "in_reply_to_status_id": 238933943146131456
        },
        "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
        "default_profile_image": False,
        "friends_count": 31,
        "screen_name": "twitterapi",
        "following": True,
        "show_all_inline_media": False
    },
    {
        "name": "Twitter",
        "profile_sidebar_fill_color": "F6F6F6",
        "profile_background_tile": True,
        "profile_sidebar_border_color": "EEEEEE",
        "profile_image_url": "http://a0.twimg.com/profile_images/2284174758/v65oai7fxn47qv9nectx_normal.png",
        "location": "San Francisco, CA",
        "created_at": "Tue Feb 20 14:35:54 +0000 2007",
        "follow_request_sent": False,
        "id_str": "783214",
        "profile_link_color": "038543",
        "is_translator": False,
        "default_profile": False,
        "favourites_count": 17,
        "contributors_enabled": True,
        "url": "http://blog.twitter.com/",
        "profile_image_url_https": "https://si0.twimg.com/profile_images/2284174758/v65oai7fxn47qv9nectx_normal.png",
        "utc_offset": -28800,
        "id": 783214,
        "profile_banner_url": "https://si0.twimg.com/brand_banners/twitter/1323368512/live",
        "profile_use_background_image": True,
        "listed_count": 72534,
        "profile_text_color": "333333",
        "lang": "en",
        "followers_count": 12788713,
        "protected": False,
        "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/378245879/Twitter_1544x2000.png",
        "geo_enabled": True,
        "description": "Always wondering what's happening. ",
        "profile_background_color": "ACDED6",
        "verified": True,
        "notifications": False,
        "time_zone": "Pacific Time (US & Canada)",
        "statuses_count": 1379,
        "status": {
            "coordinates": None,
            "created_at": "Tue Aug 21 19:04:00 +0000 2012",
            "favorited": False,
            "truncated": False,
            "id_str": "237988442338897920",
            "retweeted_status": {
                "coordinates": None,
                "created_at": "Tue Aug 21 18:51:44 +0000 2012",
                "favorited": False,
                "truncated": False,
                "id_str": "237985351858278400",
                "in_reply_to_user_id_str": None,
                "text": "Arijit Guha fought for insurance coverage, and won.\n http://t.co/ZvQ6fU2O #twitterstories http://t.co/bVYPNnV7",
                "contributors": [
                    16896060
                ],
                "retweet_count": 118,
                "id": 237985351858278400,
                "in_reply_to_status_id_str": None,
                "geo": None,
                "retweeted": False,
                "possibly_sensitive": False,
                "in_reply_to_user_id": None,
                "place": None,
                "source": "web",
                "in_reply_to_screen_name": None,
                "in_reply_to_status_id": None
            },
            "in_reply_to_user_id_str": None,
            "text": "RT @TwitterStories: Arijit Guha fought for insurance coverage, and won.\n http://t.co/ZvQ6fU2O #twitterstories http://t.co/bVYPNnV7",
            "contributors": None,
            "retweet_count": 118,
            "id": 237988442338897920,
            "in_reply_to_status_id_str": None,
            "geo": None,
            "retweeted": False,
            "possibly_sensitive": False,
            "in_reply_to_user_id": None,
            "place": None,
            "source": "web",
            "in_reply_to_screen_name": None,
            "in_reply_to_status_id": None
        },
        "profile_background_image_url": "http://a0.twimg.com/profile_background_images/378245879/Twitter_1544x2000.png",
        "default_profile_image": False,
        "friends_count": 1195,
        "screen_name": "twitter",
        "following": True,
        "show_all_inline_media": True
    }
]
fake_slugs = [
    {
        "name": "Art & Design",
        "slug": "art-design",
        "size": 20
    },
    {
        "name": "Billboard Music Awards",
        "slug": "billboard-music-awards",
        "size": 20
    },
    {
        "name": "Books",
        "slug": "books",
        "size": 20
    },
    {
        "name": "Business",
        "slug": "business",
        "size": 20
    },
    {
        "name": "CMT Awards",
        "slug": "cmt-awards",
        "size": 20
    },
    {
        "name": "Charity",
        "slug": "charity",
        "size": 20
    },
    {
        "name": "Entertainment",
        "slug": "entertainment",
        "size": 20
    },
    {
        "name": "Faith and Religion",
        "slug": "faith-and-religion",
        "size": 20
    },
    {
        "name": "Family",
        "slug": "family",
        "size": 20
    },
    {
        "name": "Fashion",
        "slug": "fashion",
        "size": 20
    },
    {
        "name": "Food & Drink",
        "slug": "food-drink",
        "size": 20
    },
    {
        "name": "Funny",
        "slug": "funny",
        "size": 20
    },
    {
        "name": "Government",
        "slug": "government",
        "size": 20
    },
    {
        "name": "Health",
        "slug": "health",
        "size": 20
    },
    {
        "name": "MLB",
        "slug": "mlb",
        "size": 20
    },
    {
        "name": "MTV Movie Awards",
        "slug": "mtv-movie-awards",
        "size": 20
    },
    {
        "name": "Music",
        "slug": "music",
        "size": 20
    },
    {
        "name": "NASCAR",
        "slug": "nascar",
        "size": 20
    },
    {
        "name": "NBA",
        "slug": "nba",
        "size": 20
    },
    {
        "name": "NHL",
        "slug": "nhl",
        "size": 20
    },
    {
        "name": "News",
        "slug": "news",
        "size": 20
    },
    {
        "name": "PGA",
        "slug": "pga",
        "size": 20
    },
    {
        "name": "Science",
        "slug": "science",
        "size": 20
    },
    {
        "name": "Sports",
        "slug": "sports",
        "size": 20
    },
    {
        "name": "Staff Picks",
        "slug": "staff-picks",
        "size": 20
    },
    {
        "name": "Technology",
        "slug": "technology",
        "size": 20
    },
    {
        "name": "Television",
        "slug": "television",
        "size": 20
    },
    {
        "name": "Travel",
        "slug": "travel",
        "size": 20
    },
    {
        "name": "Twitter",
        "slug": "twitter",
        "size": 20
    },
    {
        "name": "US Election 2012",
        "slug": "us-election-2012",
        "size": 20
    }
]
fake_user_suggestions = {
    "name": "Twitter",
    "slug": "twitter",
    "size": 20,
    "users": [
        {
            "name": "Twitter Sverige",
            "profile_sidebar_border_color": "C0DEED",
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_background_tile": False,
            "created_at": "Mon Oct 31 23:10:57 +0000 2011",
            "profile_image_url": "http://a0.twimg.com/profile_images/2284174853/63g4ld4sm6yh4sssy7wy_normal.png",
            "location": "Sweden",
            "profile_link_color": "0084B4",
            "follow_request_sent": False,
            "is_translator": False,
            "id_str": "402357141",
            "default_profile": True,
            "url": "https://twitter.com/about/translation",
            "favourites_count": 0,
            "contributors_enabled": True,
            "utc_offset": 3600,
            "id": 402357141,
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2284174853/63g4ld4sm6yh4sssy7wy_normal.png",
            "listed_count": 43,
            "profile_use_background_image": True,
            "profile_text_color": "333333",
            "protected": False,
            "lang": "sv",
            "followers_count": 55446,
            "geo_enabled": False,
            "time_zone": "Stockholm",
            "notifications": False,
            "verified": False,
            "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
            "profile_background_color": "C0DEED",
            "description": "Community-konto for Twitter i Sverige. Vi haller er uppdaterade kring vad som hander pa Twitter i Sverige.",
            "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
            "friends_count": 260,
            "statuses_count": 62,
            "default_profile_image": False,
            "show_all_inline_media": False,
            "screen_name": "twitter_se",
            "following": False
        },
        {
            "name": "Twitter Suomi",
            "profile_sidebar_border_color": "C0DEED",
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_background_tile": False,
            "created_at": "Mon Oct 31 23:05:34 +0000 2011",
            "profile_image_url": "http://a0.twimg.com/profile_images/2284174783/cwp44h4tg1mkl90cta0p_normal.png",
            "location": "Finland",
            "profile_link_color": "0084B4",
            "follow_request_sent": False,
            "is_translator": False,
            "id_str": "402354593",
            "default_profile": True,
            "url": "https://twitter.com/about/translation",
            "favourites_count": 5,
            "contributors_enabled": True,
            "utc_offset": 7200,
            "id": 402354593,
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2284174783/cwp44h4tg1mkl90cta0p_normal.png",
            "listed_count": 49,
            "profile_use_background_image": True,
            "profile_text_color": "333333",
            "protected": False,
            "lang": "fi",
            "followers_count": 64440,
            "geo_enabled": False,
            "time_zone": "Helsinki",
            "notifications": False,
            "verified": False,
            "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
            "profile_background_color": "C0DEED",
            "description": "Twitterin suomalainen yhteisotili. Yllapitajina kaannosmoderaattorit @Zedinc, @SuihinOkko, @Delzun ja @DiamonDie.",
            "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
            "friends_count": 31,
            "statuses_count": 83,
            "default_profile_image": False,
            "show_all_inline_media": False,
            "screen_name": "twitter_fi",
            "following": False
        },
        {
            "name": "Twitter Government",
            "profile_sidebar_border_color": "C0DEED",
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_background_tile": False,
            "created_at": "Sat Dec 04 23:27:01 +0000 2010",
            "profile_image_url": "http://a0.twimg.com/profile_images/2284291316/xu1u3i11ugj03en53ujr_normal.png",
            "location": "Washington, DC",
            "profile_link_color": "0084B4",
            "follow_request_sent": False,
            "is_translator": False,
            "id_str": "222953824",
            "default_profile": False,
            "url": "http://twitter.com",
            "favourites_count": 6,
            "contributors_enabled": True,
            "utc_offset": -18000,
            "id": 222953824,
            "profile_image_url_https": "https://si0.twimg.com/profile_images/2284291316/xu1u3i11ugj03en53ujr_normal.png",
            "listed_count": 888,
            "profile_use_background_image": True,
            "profile_text_color": "333333",
            "protected": True,
            "lang": "en",
            "followers_count": 149418,
            "geo_enabled": True,
            "time_zone": "Eastern Time (US & Canada)",
            "notifications": False,
            "verified": True,
            "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/378138859/townhallbg.jpg",
            "profile_background_color": "C0DEED",
            "description": "Updates from the Twitter Government and Politics team, tracking creative and effective uses of Twitter for civic engagement. RTs and examples!=political endorsements.",
            "profile_background_image_url": "http://a0.twimg.com/profile_background_images/378138859/townhallbg.jpg",
            "friends_count": 0,
            "statuses_count": 338,
            "default_profile_image": False,
            "show_all_inline_media": False,
            "screen_name": "gov",
            "following": True
        }
    ]
}
fake_fr_ids = {
    "previous_cursor": 0,
    "ids": [
        657693,
        183709371,
        7588892,
        38895958,
        22891211,
        9019482,
        14488353,
        11750202,
        12249,
        22915745,
        1249881,
        14927800,
        1523501,
        22548447,
        15062340,
        133031077,
        17874544,
        777925,
        4265731,
        27674040,
        26123649,
        9576402,
        821958,
        7852612,
        819797,
        1401881,
        8285392,
        9160152,
        795649,
        3191321,
        783214
    ],
    "previous_cursor_str": "0",
    "next_cursor": 0,
    "next_cursor_str": "0"
}
fake_creds = {
    "contributors_enabled": True,
    "created_at": "Sat May 09 17:58:22 +0000 2009",
    "default_profile": False,
    "default_profile_image": False,
    "description": "I taught your phone that thing you like.  The Mobile Partner Engineer @Twitter. ",
    "favourites_count": 588,
    "follow_request_sent": None,
    "followers_count": 10625,
    "following": None,
    "friends_count": 1181,
    "geo_enabled": True,
    "id": 38895958,
    "id_str": "38895958",
    "is_translator": False,
    "lang": "en",
    "listed_count": 190,
    "location": "San Francisco",
    "name": "Sean Cook",
    "notifications": None,
    "profile_background_color": "1A1B1F",
    "profile_background_image_url": "http://a0.twimg.com/profile_background_images/495742332/purty_wood.png",
    "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/495742332/purty_wood.png",
    "profile_background_tile": True,
    "profile_image_url": "http://a0.twimg.com/profile_images/1751506047/dead_sexy_normal.JPG",
    "profile_image_url_https": "https://si0.twimg.com/profile_images/1751506047/dead_sexy_normal.JPG",
    "profile_link_color": "2FC2EF",
    "profile_sidebar_border_color": "181A1E",
    "profile_sidebar_fill_color": "252429",
    "profile_text_color": "666666",
    "profile_use_background_image": True,
    "protected": False,
    "screen_name": "theSeanCook",
    "show_all_inline_media": True,
    "status": {
        "contributors": None,
        "coordinates": {
            "coordinates": [
                -122.45037293,
                37.76484123
            ],
            "type": "Point"
        },
        "created_at": "Tue Aug 28 05:44:24 +0000 2012",
        "favorited": False,
        "geo": {
            "coordinates": [
                37.76484123,
                -122.45037293
            ],
            "type": "Point"
        },
        "id": 240323931419062272,
        "id_str": "240323931419062272",
        "in_reply_to_screen_name": "messl",
        "in_reply_to_status_id": 240316959173009410,
        "in_reply_to_status_id_str": "240316959173009410",
        "in_reply_to_user_id": 18707866,
        "in_reply_to_user_id_str": "18707866",
        "place": {
            "attributes": {},
            "bounding_box": {
                "coordinates": [
                    [
                        [
                            -122.45778216,
                            37.75932999
                        ],
                        [
                            -122.44248216,
                            37.75932999
                        ],
                        [
                            -122.44248216,
                            37.76752899
                        ],
                        [
                            -122.45778216,
                            37.76752899
                        ]
                    ]
                ],
                "type": "Polygon"
            },
            "country": "United States",
            "country_code": "US",
            "full_name": "Ashbury Heights, San Francisco",
            "id": "866269c983527d5a",
            "name": "Ashbury Heights",
            "place_type": "neighborhood",
            "url": "http://api.twitter.com/1/geo/id/866269c983527d5a.json"
        },
        "retweet_count": 0,
        "retweeted": False,
        "source": "Twitter for  iPhone",
        "text": "@messl congrats! So happy for all 3 of you.",
        "truncated": False
    },
    "statuses_count": 2609,
    "time_zone": "Pacific Time (US & Canada)",
    "url": None,
    "utc_offset": -28800,
    "verified": False
}
fake_trends_locations = [
    {
        "country": "Sweden",
        "countryCode": "SE",
        "name": "Sweden",
        "parentid": 1,
        "placeType": {
            "code": 12,
            "name": "Country"
        },
        "url": "http://where.yahooapis.com/v1/place/23424954",
        "woeid": 23424954
    },
    {
        "country": "United States",
        "countryCode": "US",
        "name": "New Haven",
        "parentid": 23424977,
        "placeType": {
            "code": 7,
            "name": "Town"
        },
        "url": "http://where.yahooapis.com/v1/place/2458410",
        "woeid": 2458410
    },
    {
        "country": "Japan",
        "countryCode": "JP",
        "name": "Sapporo",
        "parentid": 23424856,
        "placeType": {
            "code": 7,
            "name": "Town"
        },
        "url": "http://where.yahooapis.com/v1/place/1118108",
        "woeid": 1118108
    },
    {
        "country": "United States",
        "countryCode": "US",
        "name": "Providence",
        "parentid": 23424977,
        "placeType": {
            "code": 7,
            "name": "Town"
        },
        "url": "http://where.yahooapis.com/v1/place/2477058",
        "woeid": 2477058
    },
    {
        "country": "United States",
        "countryCode": "US",
        "name": "Cincinnati",
        "parentid": 23424977,
        "placeType": {
            "code": 7,
            "name": "Town"
        },
        "url": "http://where.yahooapis.com/v1/place/2380358",
        "woeid": 2380358
    }
]
fake_trends = [
    {
        "trends": [
            {
                "name": "#ChainedToTheRhythm",
                "url": "http://twitter.com/search_queries?q=%23ChainedToTheRhythm",
                "promoted_content": None,
                "query": "%23ChainedToTheRhythm",
                "tweet_volume": 48857
            },
            {
                "name": "George Lopez",
                "url": "http://twitter.com/search_queries?q=%22George+Lopez%22",
                "promoted_content": None,
                "query": "%22George+Lopez%22",
                "tweet_volume": 90590
            },
            {
                "name": "#FelizMiercoles",
                "url": "http://twitter.com/search_queries?q=%23FelizMiercoles",
                "promoted_content": None,
                "query": "%23FelizMiercoles",
                "tweet_volume": 36103
            },
            {
                "name": "#wednesdaywisdom",
                "url": "http://twitter.com/search_queries?q=%23wednesdaywisdom",
                "promoted_content": None,
                "query": "%23wednesdaywisdom",
                "tweet_volume": 42916
            },
            {
                "name": "Tara Palmer-Tomkinson",
                "url": "http://twitter.com/search_queries?q=%22Tara+Palmer-Tomkinson%22",
                "promoted_content": None,
                "query": "%22Tara+Palmer-Tomkinson%22",
                "tweet_volume": None
            },
            {
                "name": "SLAY CAMILIZERS",
                "url": "http://twitter.com/search_queries?q=%22SLAY+CAMILIZERS%22",
                "promoted_content": None,
                "query": "%22SLAY+CAMILIZERS%22",
                "tweet_volume": 707166
            },
            {
                "name": "WORK FROM 5H",
                "url": "http://twitter.com/search_queries?q=%22WORK+FROM+5H%22",
                "promoted_content": None,
                "query": "%22WORK+FROM+5H%22",
                "tweet_volume": 54061
            },
            {
                "name": "Leyla Zana",
                "url": "http://twitter.com/search_queries?q=%22Leyla+Zana%22",
                "promoted_content": None,
                "query": "%22Leyla+Zana%22",
                "tweet_volume": None
            },
            {
                "name": "#TwoJustin",
                "url": "http://twitter.com/search_queries?q=%23TwoJustin",
                "promoted_content": None,
                "query": "%23TwoJustin",
                "tweet_volume": None
            },
            {
                "name": "#MyFirstAndLast",
                "url": "http://twitter.com/search_queries?q=%23MyFirstAndLast",
                "promoted_content": None,
                "query": "%23MyFirstAndLast",
                "tweet_volume": 63844
            },
            {
                "name": "#ValentinesDayIn3Words",
                "url": "http://twitter.com/search_queries?q=%23ValentinesDayIn3Words",
                "promoted_content": None,
                "query": "%23ValentinesDayIn3Words",
                "tweet_volume": None
            },
            {
                "name": "#ShePersisted",
                "url": "http://twitter.com/search_queries?q=%23ShePersisted",
                "promoted_content": None,
                "query": "%23ShePersisted",
                "tweet_volume": 45624
            },
            {
                "name": "#HappyJohnnyDay",
                "url": "http://twitter.com/search_queries?q=%23HappyJohnnyDay",
                "promoted_content": None,
                "query": "%23HappyJohnnyDay",
                "tweet_volume": 28560
            },
            {
                "name": "#QuartaDetremuraSDV",
                "url": "http://twitter.com/search_queries?q=%23QuartaDetremuraSDV",
                "promoted_content": None,
                "query": "%23QuartaDetremuraSDV",
                "tweet_volume": 10481
            },
            {
                "name": "#TapperDirtFile",
                "url": "http://twitter.com/search_queries?q=%23TapperDirtFile",
                "promoted_content": None,
                "query": "%23TapperDirtFile",
                "tweet_volume": None
            },
            {
                "name": "#FelizCumplePresidente",
                "url": "http://twitter.com/search_queries?q=%23FelizCumplePresidente",
                "promoted_content": None,
                "query": "%23FelizCumplePresidente",
                "tweet_volume": 15276
            },
            {
                "name": "#MeCasoSiMeDices",
                "url": "http://twitter.com/search_queries?q=%23MeCasoSiMeDices",
                "promoted_content": None,
                "query": "%23MeCasoSiMeDices",
                "tweet_volume": None
            },
            {
                "name": "#FebreroZamorista",
                "url": "http://twitter.com/search_queries?q=%23FebreroZamorista",
                "promoted_content": None,
                "query": "%23FebreroZamorista",
                "tweet_volume": None
            },
            {
                "name": "#NinguemSabeMasEuJa",
                "url": "http://twitter.com/search_queries?q=%23NinguemSabeMasEuJa",
                "promoted_content": None,
                "query": "%23NinguemSabeMasEuJa",
                "tweet_volume": 12856
            },
            {
                "name": "#HappyChunghaDay",
                "url": "http://twitter.com/search_queries?q=%23HappyChunghaDay",
                "promoted_content": None,
                "query": "%23HappyChunghaDay",
                "tweet_volume": 16480
            },
            {
                "name": "#DiaDeLaPiscola",
                "url": "http://twitter.com/search_queries?q=%23DiaDeLaPiscola",
                "promoted_content": None,
                "query": "%23DiaDeLaPiscola",
                "tweet_volume": None
            },
            {
                "name": "#UnBuenTaco",
                "url": "http://twitter.com/search_queries?q=%23UnBuenTaco",
                "promoted_content": None,
                "query": "%23UnBuenTaco",
                "tweet_volume": None
            },
            {
                "name": "#PMQs",
                "url": "http://twitter.com/search_queries?q=%23PMQs",
                "promoted_content": None,
                "query": "%23PMQs",
                "tweet_volume": 20406
            },
            {
                "name": "#InteractFalando",
                "url": "http://twitter.com/search_queries?q=%23InteractFalando",
                "promoted_content": None,
                "query": "%23InteractFalando",
                "tweet_volume": None
            },
            {
                "name": "#LIZAonTWBA",
                "url": "http://twitter.com/search_queries?q=%23LIZAonTWBA",
                "promoted_content": None,
                "query": "%23LIZAonTWBA",
                "tweet_volume": 68066
            },
            {
                "name": "#nldebat",
                "url": "http://twitter.com/search_queries?q=%23nldebat",
                "promoted_content": None,
                "query": "%23nldebat",
                "tweet_volume": None
            },
            {
                "name": "#ConselhosDeUmTrouxa",
                "url": "http://twitter.com/search_queries?q=%23ConselhosDeUmTrouxa",
                "promoted_content": None,
                "query": "%23ConselhosDeUmTrouxa",
                "tweet_volume": 11419
            },
            {
                "name": "#PBBKiligOverload",
                "url": "http://twitter.com/search_queries?q=%23PBBKiligOverload",
                "promoted_content": None,
                "query": "%23PBBKiligOverload",
                "tweet_volume": 70766
            },
            {
                "name": "#MiMejorPiropoParaTi",
                "url": "http://twitter.com/search_queries?q=%23MiMejorPiropoParaTi",
                "promoted_content": None,
                "query": "%23MiMejorPiropoParaTi",
                "tweet_volume": None
            },
            {
                "name": "#8Feb",
                "url": "http://twitter.com/search_queries?q=%238Feb",
                "promoted_content": None,
                "query": "%238Feb",
                "tweet_volume": None
            },
            {
                "name": "#LoveBeyondFlags",
                "url": "http://twitter.com/search_queries?q=%23LoveBeyondFlags",
                "promoted_content": None,
                "query": "%23LoveBeyondFlags",
                "tweet_volume": None
            },
            {
                "name": "#MSWL",
                "url": "http://twitter.com/search_queries?q=%23MSWL",
                "promoted_content": None,
                "query": "%23MSWL",
                "tweet_volume": None
            },
            {
                "name": "#SoMeArrependoDe",
                "url": "http://twitter.com/search_queries?q=%23SoMeArrependoDe",
                "promoted_content": None,
                "query": "%23SoMeArrependoDe",
                "tweet_volume": None
            },
        ],
        "as_of": "2017-02-08T16:18:18Z",
        "created_at": "2017-02-08T16:10:33Z",
        "locations": [
            {
                "name": "Worldwide",
                "woeid": 1
            }
        ]
    }
]
fake_search_data = {
    "statuses": [
        {
            "coordinates": None,
            "favorited": False,
            "truncated": False,
            "created_at": "Mon Sep 24 03:35:21 +0000 2012",
            "id_str": "250075927172759552",
            "entities": {
                "urls": [

                ],
                "hashtags": [
                    {
                        "text": "freebandnames",
                        "indices": [
                            20,
                            34
                        ]
                    }
                ],
                "user_mentions": [

                ]
            },
            "in_reply_to_user_id_str": None,
            "contributors": None,
            "text": "Aggressive Ponytail #freebandnames",
            "metadata": {
                "iso_language_code": "en",
                "result_type": "recent"
            },
            "retweet_count": 0,
            "in_reply_to_status_id_str": None,
            "id": 250075927172759552,
            "geo": None,
            "retweeted": False,
            "in_reply_to_user_id": None,
            "place": None,
            "user": {
                "profile_sidebar_fill_color": "DDEEF6",
                "profile_sidebar_border_color": "C0DEED",
                "profile_background_tile": False,
                "name": "Sean Cummings",
                "profile_image_url": "http://a0.twimg.com/profile_images/2359746665/1v6zfgqo8g0d3mk7ii5s_normal.jpeg",
                "created_at": "Mon Apr 26 06:01:55 +0000 2010",
                "location": "LA, CA",
                "follow_request_sent": None,
                "profile_link_color": "0084B4",
                "is_translator": False,
                "id_str": "137238150",
                "entities": {
                    "url": {
                        "urls": [
                            {
                                "expanded_url": None,
                                "url": "",
                                "indices": [
                                    0,
                                    0
                                ]
                            }
                        ]
                    },
                    "description": {
                        "urls": [

                        ]
                    }
                },
                "default_profile": True,
                "contributors_enabled": False,
                "favourites_count": 0,
                "url": None,
                "profile_image_url_https": "https://si0.twimg.com/profile_images/2359746665/1v6zfgqo8g0d3mk7ii5s_normal.jpeg",
                "utc_offset": -28800,
                "id": 137238150,
                "profile_use_background_image": True,
                "listed_count": 2,
                "profile_text_color": "333333",
                "lang": "en",
                "followers_count": 70,
                "protected": False,
                "notifications": None,
                "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
                "profile_background_color": "C0DEED",
                "verified": False,
                "geo_enabled": True,
                "time_zone": "Pacific Time (US & Canada)",
                "description": "Born 330 Live 310",
                "default_profile_image": False,
                "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
                "statuses_count": 579,
                "friends_count": 110,
                "following": None,
                "show_all_inline_media": False,
                "screen_name": "sean_cummings"
            },
            "in_reply_to_screen_name": None,
            "source": "Twitter for Mac",
            "in_reply_to_status_id": None
        },
        {
            "coordinates": None,
            "favorited": False,
            "truncated": False,
            "created_at": "Fri Sep 21 23:40:54 +0000 2012",
            "id_str": "249292149810667520",
            "entities": {
                "urls": [

                ],
                "hashtags": [
                    {
                        "text": "FreeBandNames",
                        "indices": [
                            20,
                            34
                        ]
                    }
                ],
                "user_mentions": [

                ]
            },
            "in_reply_to_user_id_str": None,
            "contributors": None,
            "text": "Thee Namaste Nerdz. #FreeBandNames",
            "metadata": {
                "iso_language_code": "pl",
                "result_type": "recent"
            },
            "retweet_count": 0,
            "in_reply_to_status_id_str": None,
            "id": 249292149810667520,
            "geo": None,
            "retweeted": False,
            "in_reply_to_user_id": None,
            "place": None,
            "user": {
                "profile_sidebar_fill_color": "DDFFCC",
                "profile_sidebar_border_color": "BDDCAD",
                "profile_background_tile": True,
                "name": "Chaz Martenstein",
                "profile_image_url": "http://a0.twimg.com/profile_images/447958234/Lichtenstein_normal.jpg",
                "created_at": "Tue Apr 07 19:05:07 +0000 2009",
                "location": "Durham, NC",
                "follow_request_sent": None,
                "profile_link_color": "0084B4",
                "is_translator": False,
                "id_str": "29516238",
                "entities": {
                    "url": {
                        "urls": [
                            {
                                "expanded_url": None,
                                "url": "http://bullcityrecords.com/wnng/",
                                "indices": [
                                    0,
                                    32
                                ]
                            }
                        ]
                    },
                    "description": {
                        "urls": [

                        ]
                    }
                },
                "default_profile": False,
                "contributors_enabled": False,
                "favourites_count": 8,
                "url": "http://bullcityrecords.com/wnng/",
                "profile_image_url_https": "https://si0.twimg.com/profile_images/447958234/Lichtenstein_normal.jpg",
                "utc_offset": -18000,
                "id": 29516238,
                "profile_use_background_image": True,
                "listed_count": 118,
                "profile_text_color": "333333",
                "lang": "en",
                "followers_count": 2052,
                "protected": False,
                "notifications": None,
                "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/9423277/background_tile.bmp",
                "profile_background_color": "9AE4E8",
                "verified": False,
                "geo_enabled": False,
                "time_zone": "Eastern Time (US & Canada)",
                "description": "You will come to Durham, North Carolina. I will sell you some records then, here in Durham, North Carolina. Fun will happen.",
                "default_profile_image": False,
                "profile_background_image_url": "http://a0.twimg.com/profile_background_images/9423277/background_tile.bmp",
                "statuses_count": 7579,
                "friends_count": 348,
                "following": None,
                "show_all_inline_media": True,
                "screen_name": "bullcityrecords"
            },
            "in_reply_to_screen_name": None,
            "source": "web",
            "in_reply_to_status_id": None
        },
        {
            "coordinates": None,
            "favorited": False,
            "truncated": False,
            "created_at": "Fri Sep 21 23:30:20 +0000 2012",
            "id_str": "249289491129438208",
            "entities": {
                "urls": [

                ],
                "hashtags": [
                    {
                        "text": "freebandnames",
                        "indices": [
                            29,
                            43
                        ]
                    }
                ],
                "user_mentions": [

                ]
            },
            "in_reply_to_user_id_str": None,
            "contributors": None,
            "text": "Mexican Heaven, Mexican Hell #freebandnames",
            "metadata": {
                "iso_language_code": "en",
                "result_type": "recent"
            },
            "retweet_count": 0,
            "in_reply_to_status_id_str": None,
            "id": 249289491129438208,
            "geo": None,
            "retweeted": False,
            "in_reply_to_user_id": None,
            "place": None,
            "user": {
                "profile_sidebar_fill_color": "99CC33",
                "profile_sidebar_border_color": "829D5E",
                "profile_background_tile": False,
                "name": "Thomas John Wakeman",
                "profile_image_url": "http://a0.twimg.com/profile_images/2219333930/Froggystyle_normal.png",
                "created_at": "Tue Sep 01 21:21:35 +0000 2009",
                "location": "Kingston New York",
                "follow_request_sent": None,
                "profile_link_color": "D02B55",
                "is_translator": False,
                "id_str": "70789458",
                "entities": {
                    "url": {
                        "urls": [
                            {
                                "expanded_url": None,
                                "url": "",
                                "indices": [
                                    0,
                                    0
                                ]
                            }
                        ]
                    },
                    "description": {
                        "urls": [

                        ]
                    }
                },
                "default_profile": False,
                "contributors_enabled": False,
                "favourites_count": 19,
                "url": None,
                "profile_image_url_https": "https://si0.twimg.com/profile_images/2219333930/Froggystyle_normal.png",
                "utc_offset": -18000,
                "id": 70789458,
                "profile_use_background_image": True,
                "listed_count": 1,
                "profile_text_color": "3E4415",
                "lang": "en",
                "followers_count": 63,
                "protected": False,
                "notifications": None,
                "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme5/bg.gif",
                "profile_background_color": "352726",
                "verified": False,
                "geo_enabled": False,
                "time_zone": "Eastern Time (US & Canada)",
                "description": "Science Fiction Writer, sort of. Likes Superheroes, Mole People, Alt. Timelines.",
                "default_profile_image": False,
                "profile_background_image_url": "http://a0.twimg.com/images/themes/theme5/bg.gif",
                "statuses_count": 1048,
                "friends_count": 63,
                "following": None,
                "show_all_inline_media": False,
                "screen_name": "MonkiesFist"
            },
            "in_reply_to_screen_name": None,
            "source": "web",
            "in_reply_to_status_id": None
        },
        {
            "coordinates": None,
            "favorited": False,
            "truncated": False,
            "created_at": "Fri Sep 21 22:51:18 +0000 2012",
            "id_str": "249279667666817024",
            "entities": {
                "urls": [

                ],
                "hashtags": [
                    {
                        "text": "freebandnames",
                        "indices": [
                            20,
                            34
                        ]
                    }
                ],
                "user_mentions": [

                ]
            },
            "in_reply_to_user_id_str": None,
            "contributors": None,
            "text": "The Foolish Mortals #freebandnames",
            "metadata": {
                "iso_language_code": "en",
                "result_type": "recent"
            },
            "retweet_count": 0,
            "in_reply_to_status_id_str": None,
            "id": 249279667666817024,
            "geo": None,
            "retweeted": False,
            "in_reply_to_user_id": None,
            "place": None,
            "user": {
                "profile_sidebar_fill_color": "BFAC83",
                "profile_sidebar_border_color": "615A44",
                "profile_background_tile": True,
                "name": "Marty Elmer",
                "profile_image_url": "http://a0.twimg.com/profile_images/1629790393/shrinker_2000_trans_normal.png",
                "created_at": "Mon May 04 00:05:00 +0000 2009",
                "location": "Wisconsin, USA",
                "follow_request_sent": None,
                "profile_link_color": "3B2A26",
                "is_translator": False,
                "id_str": "37539828",
                "entities": {
                    "url": {
                        "urls": [
                            {
                                "expanded_url": None,
                                "url": "http://www.omnitarian.me",
                                "indices": [
                                    0,
                                    24
                                ]
                            }
                        ]
                    },
                    "description": {
                        "urls": [

                        ]
                    }
                },
                "default_profile": False,
                "contributors_enabled": False,
                "favourites_count": 647,
                "url": "http://www.omnitarian.me",
                "profile_image_url_https": "https://si0.twimg.com/profile_images/1629790393/shrinker_2000_trans_normal.png",
                "utc_offset": -21600,
                "id": 37539828,
                "profile_use_background_image": True,
                "listed_count": 52,
                "profile_text_color": "000000",
                "lang": "en",
                "followers_count": 608,
                "protected": False,
                "notifications": None,
                "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/106455659/rect6056-9.png",
                "profile_background_color": "EEE3C4",
                "verified": False,
                "geo_enabled": False,
                "time_zone": "Central Time (US & Canada)",
                "description": "Cartoonist, Illustrator, and T-Shirt connoisseur",
                "default_profile_image": False,
                "profile_background_image_url": "http://a0.twimg.com/profile_background_images/106455659/rect6056-9.png",
                "statuses_count": 3575,
                "friends_count": 249,
                "following": None,
                "show_all_inline_media": True,
                "screen_name": "Omnitarian"
            },
            "in_reply_to_screen_name": None,
            "source": "Twitter for iPhone",
            "in_reply_to_status_id": None
        }
    ],
    "search_metadata": {
        "max_id": 250126199840518145,
        "since_id": 24012619984051000,
        "refresh_url": "?since_id=250126199840518145&q=%23freebandnames&result_type=mixed&include_entities=1",
        "next_results": "?max_id=249279667666817023&q=%23freebandnames&count=4&include_entities=1&result_type=mixed",
        "count": 4,
        "completed_in": 0.035,
        "since_id_str": "24012619984051000",
        "query": "%23freebandnames",
        "max_id_str": "250126199840518145"
    }
}


class MockTwitter:
    def __init__(self):
        self.home_timeline = 15
        self.user_list_size = 100
        self.list_member_fail = False
        self.did_not_back_off = False
        self.search_query_too_long = False
        self.create_list_calls = 15
        self.create_friends = 15
        self.user_suggestions = 15
        self.user_suggestions_by_slug = 15
        self.credentials = 15
        self.user_timeline = 180
        self.lookup = TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE
        self.list_statuses = TWITTER_MAX_NUMBER_OF_LISTS
        self.followers_ids = 15
        self.friends_ids = 15
        self.followers_list = 15
        self.friends_list = 15
        self.trends = 15
        self.place_trends = 15
        self.closest = 75
        self.search_queries = 180

    def get_followers_ids(self, **kwargs):
        if self.followers_ids == 0:
            raise TwythonRateLimitError('501', 501)
        self.followers_ids -= 1
        if self.followers_ids < 0:
            self.did_not_back_off = True
        return fake_fr_ids

    def get_friends_ids(self, **kwargs):
        if self.friends_ids == 0:
            raise TwythonRateLimitError('501', 501)
        self.friends_ids -= 1
        if self.friends_ids < 0:
            self.did_not_back_off = True
        return fake_fr_ids

    def get_friends_list(self, **kwargs):
        if self.friends_list == 0:
            raise TwythonRateLimitError('501', 501)
        self.friends_list -= 1
        if self.friends_list < 0:
            self.did_not_back_off = True
        return fr_list

    def get_followers_list(self, **kwargs):
        if self.followers_list == 0:
            raise TwythonRateLimitError('501', 501)
        self.followers_list -= 1
        if self.followers_list < 0:
            self.did_not_back_off = True
        return fr_list

    def get_home_timeline(self, **kwargs):
        if self.home_timeline == 0:
            raise TwythonRateLimitError('501', 501)
        self.home_timeline -= 1
        if self.home_timeline < 0:
            self.did_not_back_off = True
        if random.uniform(0.0, 1.0) < 0.5:
            # randomly break the crawler
            print "Sent broken data"
            return broken_tweets
        return fake_tweets

    def create_list_members(self, **kwargs):
        if len(kwargs['user_id']) > self.user_list_size:
            self.list_member_fail = True
        if random.choice([True, False]):
            raise Exception('test error')
        return {'id': 5}

    def create_list(self, **kwargs):
        if self.create_list_calls == 0:
            raise TwythonRateLimitError('501', 501)
        self.create_list_calls -= 1
        if self.create_list_calls < 0:
            self.did_not_back_off = True
        return fake_list

    def create_friendship(self, **kwargs):
        if self.create_friends == 0:
            raise TwythonRateLimitError('501', 501)
        if self.create_friends < 0:
            self.did_not_back_off = True
        self.create_friends -= 1

    def get_user_suggestions(self, **kwargs):
        if self.user_suggestions == 0:
            raise TwythonRateLimitError('501', 501)
        self.user_suggestions -= 1
        if self.user_suggestions < 0:
            self.did_not_back_off = True
        return fake_slugs

    def verify_credentials(self, **kwargs):
        if self.credentials == 0:
            raise TwythonRateLimitError('501', 501)
        self.credentials -= 1
        if self.credentials < 0:
            self.did_not_back_off = True
        return fake_creds

    def get_user_suggestions_by_slug(self, **kwargs):
        if self.user_suggestions_by_slug == 0:
            raise TwythonRateLimitError('501', 501)
        self.user_suggestions_by_slug -= 1
        if self.user_suggestions_by_slug < 0:
            self.did_not_back_off = True
        throw = random.uniform(0.0, 1.0) < 0.3
        if throw:
            raise TwythonError('not found', 404)
        return fake_user_suggestions

    def get_user_timeline(self, **kwargs):
        if self.user_timeline == 0:
            raise TwythonRateLimitError('501', 501)
        self.user_timeline -= 1
        if self.user_timeline < 0:
            self.did_not_back_off = True
        if random.uniform(0.0, 1.0) < 0.5:
            # randomly break the crawler
            print "Sent broken data"
            return broken_tweets
        return fake_tweets

    def get_list_statuses(self, **kwargs):
        if self.list_statuses == 0:
            raise TwythonRateLimitError('501', 501)
        self.list_statuses -= 1
        if self.list_statuses < 0:
            self.did_not_back_off = True
        if random.uniform(0.0, 1.0) < 0.5:
            # randomly break the crawler
            print "Sent broken data"
            return broken_tweets
        return fake_tweets

    def lookup_user(self, **kwargs):
        if self.lookup == 0:
            raise TwythonRateLimitError('501', 501)
        self.lookup -= 1
        if self.lookup < 0:
            self.did_not_back_off = True
        if random.uniform(0.0, 1.0) < 0.15:
            print "Sent incomplete data"
            return {'user': {'id': 123}}
        return fake_lookup_data

    def add_list_member(self, **kwargs):
        return

    def get_available_trends(self):
        if self.trends == 0:
            raise TwythonRateLimitError('501', 501)
        self.trends -= 1
        if self.trends < 0:
            self.did_not_back_off = True
        return fake_trends_locations

    def get_place_trends(self, **kwargs):
        if self.place_trends == 0:
            raise TwythonRateLimitError('501', 501)
        self.place_trends -= 1
        if self.place_trends < 0:
            self.did_not_back_off = True
        return fake_trends

    def get_closest_trends(self, **kwargs):
        if self.closest == 0:
            raise TwythonRateLimitError('501', 501)
        self.closest -= 1
        if self.closest < 0:
            self.did_not_back_off = True
        return fake_trends

    def search(self, **kwargs):
        if len(kwargs) > 500:
            self.search_query_too_long = True
        if self.search_queries == 0:
            raise TwythonRateLimitError('501', 501)
        self.search_queries -= 1
        if self.search_queries < 0:
            self.did_not_back_off = True
        return fake_search_data

    def passed(self):
        return len(self.get_failures()) == 0

    def get_failures(self):
        attr = self.__dict__
        return [k for k in attr if (isinstance(attr[k], int) and attr[k] < 0) or attr[k] == True]


class Mock_Stream:
    def __init__(self, streamer):
        self.streamer = streamer

    def filter(self, **kwargs):
        fail = random.uniform(0.0, 1.0) < 0.1
        if fail:
            self.streamer.on_error(123, [])
        else:
            self.streamer.on_success(fake_tweets)
    def sample(self):
        fail = random.uniform(0.0, 1.0) < 0.1
        if fail:
            self.streamer.on_error(123, [])
        else:
            self.streamer.on_success(fake_tweets)


class Mock_Twitter_Stream:
    def __init__(self, *args):
        self._callback = None
        self._error_handler = None
        self.statuses = Mock_Stream(self)

    def set_callback(self, callback):
        self._callback = callback

    def set_error_handler(self, handler):
        self._error_handler = handler

    def on_success(self, data):
        if data:
            self._callback(data)

    def on_error(self, status_code, data):
        self._error_handler()

    def disconnect(self):
        pass
