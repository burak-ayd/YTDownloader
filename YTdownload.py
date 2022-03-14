import argparse
import sys
from youtubeDownloader import Youtube


parser = argparse.ArgumentParser(description="Selenium ile Youtube indirme programı" , epilog="Korumalı içerikleri indiremez")
parser.add_argument( "-u" , help="Video URL" , metavar='url' , dest="url" , type=str , required=True)
parser.add_argument( "-q" , help="Video Kalitesi için=>(1080p-720p-480p-360p) |||| Sadece Ses İçin=>Audio" , metavar='quality' , dest="quality" , type=str )
args = parser.parse_args()

if(args.quality=="Audio"):
    obj = Youtube(args.url)
    obj.download_audio()
else:
    obj = Youtube(args.url)
    obj.download_video(args.quality)

