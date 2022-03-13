import argparse
import sys

parser = argparse.ArgumentParser(description="A Python script to download youtube videos withhelp of ffmpeg" , epilog="Download restricted videos can't be download")
parser.add_argument( "-u" , help="Video URL" , metavar='url' , dest="url" , type=str , required=True)
parser.add_argument( "-v" , help="Download Video" , metavar='video' , dest="video" , type=int )
parser.add_argument( "-q" , help="Video (1080-720-480-360)" , metavar='quality' , dest="quality" , type=int )
parser.add_argument( "-a" , help="Download Only Audio" , metavar='audio' , dest="audio" , type=int)
args = parser.parse_args()

if args.vtag == None and args.atag == None:
    print("Lütlen indirmek istediğiniz formatı seçiniz")
    exit(1)