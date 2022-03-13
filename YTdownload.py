import argparse
import sys
from youtubeDownloader import Youtube


parser = argparse.ArgumentParser(description="A Python script to download youtube videos withhelp of ffmpeg" , epilog="Download restricted videos can't be download")
parser.add_argument( "-u" , help="Video URL" , metavar='url' , dest="url" , type=str , required=True)
parser.add_argument( "-v" , help="Download Video" , metavar='video' , dest="video" , type=int )
parser.add_argument( "-q" , help="Video Quality (1080-720-480-360)" , metavar='quality' , dest="quality" , type=int )
parser.add_argument( "-a" , help="Download Only Audio" , metavar='audio' , dest="audio" , type=bool)
args = parser.parse_args()

if(args.audio==True):
    obj = Youtube(args.url)
    obj.download_audio()
else:
    obj = Youtube(args.url)
    obj.download_video(args.quality)

