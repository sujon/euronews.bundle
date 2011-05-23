# -*- coding: utf-8 -*-
import re

TITLE = 'euronews'
RSS_FEED = 'http://gdata.youtube.com/feeds/base/users/nocommenttv/uploads?alt=rss&v=2&orderby=published&client=ytapi-youtube-profile'
EUROLIVEF = 'http://www.euronews.net/media/player_live_1_7.swf?lng=fr'
EUROLIVE = 'http://www.euronews.net/media/player_live_1_7.swf?lng=en'
YT_VIDEO_FORMATS = ['Standard', 'Medium', 'High', '720p', '1080p']
YT_FMT = [34, 18, 35, 22, 37]
YT_VIDEO_PAGE = 'http://www.youtube.com/watch?v=%s'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################
def Start():
    Plugin.AddPrefixHandler('/video/euronews', MainMenu, TITLE, ICON, ART)
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

    MediaContainer.title1 = TITLE
    MediaContainer.art = R(ART)
    MediaContainer.viewGroup = 'InfoList'

    DirectoryItem.thumb = R(ICON)
    WebVideoItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)

####################################################################################################
def MainMenu():
    dir = MediaContainer()
    dir.Append(WebVideoItem(EUROLIVE, title='Euronews live stream (English)'))
    dir.Append(WebVideoItem(EUROLIVEF, title='Euronews live stream (French)'))
    dir.Append(Function(DirectoryItem(Nocomment, title='Browse No Comment Reports')))
    dir.Append(PrefsItem(title='Preferences', thumb=R('icon-prefs.png')))
    return dir

####################################################################################################
def Nocomment(sender):
    dir = MediaContainer(httpCookies=HTTP.GetCookiesForURL('http://www.youtube.com/'))
    for item in HTML.ElementFromURL(RSS_FEED).xpath('//item'):
        date = item.xpath('./pubdate')[0].text.replace('+0000', '')
        title = item.xpath('./title')[0].text.replace(' - no comment', '')
        thumb = item.xpath('./description')[0].get('src')
        video_id = item.xpath('./guid')[0].text.replace('tag:youtube.com,2008:video:', '')
        dir.Append(Function(VideoItem(PlayVideo, title, summary=date, thumb=thumb), video_id=video_id))
    return dir

####################################################################################################
def PlayVideo(sender, video_id):
    yt_page = HTTP.Request(YT_VIDEO_PAGE % (video_id), cacheTime=1).content

    fmt_url_map = re.findall('"fmt_url_map".+?"([^"]+)', yt_page)[0]
    fmt_url_map = fmt_url_map.replace('\/', '/').split(',')

    fmts = []
    fmts_info = {}

    for f in fmt_url_map:
        (fmt, url) = f.split('|')
        fmts.append(fmt)
        fmts_info[str(fmt)] = url

    index = YT_VIDEO_FORMATS.index(Prefs['yt_fmt'])
    if YT_FMT[index] in fmts:
        fmt = YT_FMT[index]
    else:
        for i in reversed( range(0, index+1) ):
            if str(YT_FMT[i]) in fmts:
                fmt = YT_FMT[i]
                break
            else:
                fmt = 5

    url = (fmts_info[str(fmt)]).decode('unicode_escape')
    return Redirect(url)
