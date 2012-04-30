# -*- coding: utf-8 -*-
import re

TITLE = 'euronews'
EUROLIVE_EN = 'http://www.euronews.com/news/streaming-live/'
EUROLIVE_FR = 'http://fr.euronews.com/infos/en-direct/'

RSS_FEED = 'http://gdata.youtube.com/feeds/base/users/nocommenttv/uploads?alt=rss&v=2&orderby=published&client=ytapi-youtube-profile'
YT_VIDEO_PAGE = 'http://www.youtube.com/watch?v=%s'

ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################
def Start():

	Plugin.AddPrefixHandler('/video/euronews', MainMenu, TITLE, ICON, ART)
	Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	ObjectContainer.view_group = 'InfoList'

	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)

####################################################################################################
def MainMenu():

	oc = ObjectContainer()
	oc.add(VideoClipObject(url = EUROLIVE_EN, title = 'Euronews live stream (English)'))
	oc.add(VideoClipObject(url = EUROLIVE_FR, title = 'Euronews live stream (French)'))
	oc.add(DirectoryObject(key = Callback(NoComment), title = 'Browse No Comment Reports'))
	return oc

####################################################################################################
def NoComment():

	oc = ObjectContainer()

	for item in HTML.ElementFromURL(RSS_FEED).xpath('//item'):
		date = item.xpath('./pubdate')[0].text.replace('+0000', '')
		title = item.xpath('./title')[0].text.replace(' - no comment', '')
		video_id = item.xpath('./guid')[0].text.replace('tag:youtube.com,2008:video:', '')

		description_text = item.xpath('./description/text()')[0]
		description_node = HTML.ElementFromString(String.Unquote(description_text))
		description = description_node.xpath('//span/text()')[0].split('|')[-1].replace('www.euronews.net','').strip()
		thumb = description_node.xpath('//img')[0].get('src')

		oc.add(VideoClipObject(
			url = YT_VIDEO_PAGE % video_id, 
			title = title,
			summary = description,
			thumb = thumb,
			originally_available_at = Datetime.ParseDate(date)))

	return oc
