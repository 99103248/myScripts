#!/usr/bin/python
###################################################
# python script to download youtube video.
#
# It supports user choosing different video 
# quality/format to download.
#
# Version: 1.0
#
# Kent 2010.10.19 
# Email: kent dot yuan at gmail dot com.
#
# Todo:
# - output directory as parameter
# - batch downloading
#
###################################################

import urllib2, re ,os, sys

# lq,mq,hq are at this moment not used. In later version (if there was), batch downloading would be 
# supported. Then they will make sense. 
lq = ('34','0','5','13','17')
mq = ('6','35','18')
hq = ('37','32')
#--------------------------------------
quality ={
            
    '34' :  ('flv', '320x240', 'Stereo 44KHz MP3'),
    '0'  :  ('flv', '320x240', 'Mono 22KHz MP3'),
    '5'  :  ('flv', '320x240', 'Mono 44KHz MP3'),
    '13' :  ('3gp', '176x144', 'Stereo 8KHz'),
    '17' :  ('3gp', '176x144', 'Mono 22KHz'),

    '6'  :  ('flv', '480x360', 'Mono 44KHz MP3'),
    '35' :  ('flv', '640x380', 'Stereo 44KHz MP3'),
    '18' :  ('mp4', '480x360', 'Stereo 44KHz AAC H.264'),

    '22' :  ('mp4', '1280x720', 'Stereo 44KHz AAC H.264'),
    '37' :  ('mp4', '1920x1080', 'Stereo 44KHz AAC H.264')
}



def usage():
    print "YouTube Video Downloader"
    print "Usage:"
    print "\t" + sys.argv[0] + " <YouTube Link>"


def __output(flag, msg):
    if flag == 'i':
        print "[INFO] %s" % msg 
    elif flag == 'e':
        print "\n[ERROR] %s\n" % msg 
    elif flag == 'n':
        print "    %s" % msg
    elif flag == 's':
        print "\n========================================\n"

def __inputValid(n, dlMap):

    if not n:
        return False

    if n=='x':
        __output('i','User aborted')
        sys.exit()
    else:
        try:
            return dlMap.has_key(dlMap.keys()[int(n)-1])
        except:
            __output('e', 'Invalid user input')
            return False


#decode url function
_ud = re.compile('%([0-9a-hA-H]{2})', re.MULTILINE)
urldecode = lambda x: _ud.sub( lambda m: chr( int( m.group(1), 16 ) ) ,x ) 

        
def getVideoLinks(ytLink):

    #get video id
    try:
        vid = ytLink.split("v=")[1].split("&")[0]
        videoInfo =  urllib2.urlopen("http://www.youtube.com/get_video_info?video_id="+vid).read()
    except:
        __output('e',"video link cannot be parsed. Please check the youtube link")
        sys.exit(1)

    regex="""fmt_url_map=(.*?)&"""

    p = re.compile(regex,re.DOTALL)
    m = p.search(videoInfo)

    if not m:
        __output('e','Parsing video info failed. Link:'+ ytLink)
        sys.exit(1) 
    
    #building up the dlMap
    dlinks = urldecode(m.group(1)).split(",")
    dlMap = {}
    for item in dlinks:
        dlMap[item.split('|')[0]] = urldecode(item.split('|')[1])
    

    #waiting user's input of video quality
    n = None
    while ( not __inputValid(n,dlMap)):    
        __output('i', 'Available video format/qualities:')
        __output('s','===')
        for k in dlMap.keys():
            if quality.has_key(k):
                __output('n', str(dlMap.keys().index(k)+1) + " - " + str(quality[k]))
        __output('n', 'x - Quit')
        __output('s','===')
        n = raw_input("Choose the format and quality of the video you wanna download:")
    
    qIdx = dlMap.keys()[int(n)-1]
    filename = vid + "." + quality[qIdx][0]
    url = dlMap[qIdx]
    cmd = 'wget -O ~/Desktop/'+filename+' "' + url + '"'
    __output('s','===')
    __output('i','downloading ' + '-'.join(quality[qIdx]) + ' as ' + filename)
    __output('s','===')
    #print cmd
    os.system(cmd)



if __name__ == '__main__':
    if sys.argv.__len__()<2 or not sys.argv[1]:
        usage()
        sys.exit(1)
    else:
        getVideoLinks(sys.argv[1])

