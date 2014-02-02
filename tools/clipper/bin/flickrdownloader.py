#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import sys
from pprint import pprint

class FlickrClient(object):
    
    def __init__(self, apikey, apisecret, userid):
        self.__apikey = apikey
        self.__apisecret = apisecret
        self.__userid = userid
        self.__baseurl = u'http://api.flickr.com/services/rest/?method='

    def getuserid(self):
        return self.__userid
        
    def setuserid(self, userid):
        self.__userid = userid
        
    userid = property(getuserid, setuserid)
    
    def getbytag(self, tag, page=1, ismine=True, cconly=True, size='m'):
        url = self.__baseurl + u'flickr.photos.search&api_key=%s&tags=%s&extras=url_%s&page=%s&format=json&nojsoncallback=1' % (self.__apikey, tag, size, page)
        if ismine:
            url += '&user_id=%s' % (self.__userid,)
        if cconly:
            url += '&license=4'
        response = urllib2.urlopen(url.encode('utf-8'))
        parsed = json.loads(response.read())
        return parsed

    def downloadphotos(self, photolist, targetdir, size='m', verbose=False):
        urls = self.__buildphotourls(photolist, size=size)    
        for url in urls:
            if verbose:
                print('download: %s' % (url,))
                
            response = urllib2.urlopen(url)
            f = open(targetdir + '/' + url.split('/')[-1], 'wb')
            f.write(response.read())
            f.close()
            
    def __buildphotourls(self, photolist, size='m'):
        urls = []
        key = 'url_%s' % (size,)
        for p in photolist:
            urls.append(p[key])
            
        return urls
            
if __name__ == '__main__':
    try:
        apikey = 'cf34b6d0fc8d5d2924ba67c7158739a3'
        apisecret = 'eca90abc0e259384'
        userid = '95962563@N02'
        flickr = FlickrClient(apikey, apisecret, userid)
        tag = u'福井県'
        #tag = u'石神井公園'
        #tag = u'cat'
        print('search by %s' % (tag,))
        dstdir = './static/negative/images/other'
        ret = flickr.getbytag(tag, ismine=False, cconly=False)
        pagenum = int(ret['photos']['pages'])
        print('total pages: %s' % (pagenum,))
        total = ret['photos']['total']
        print('total photos: %s' % (total,))
        pagenum = 10
        for i in xrange(1, pagenum + 1):
            print('page %s' % (i,))
            ret = flickr.getbytag(tag, page=i, ismine=False, cconly=False)
            flickr.downloadphotos(ret['photos']['photo'], dstdir, verbose=True)
            
        print('complete.')
    except KeyboardInterrupt as e:
        print(e)
        sys.exit(-1)
