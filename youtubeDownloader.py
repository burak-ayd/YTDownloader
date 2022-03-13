from msilib.schema import Class
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from json import load, dumps
from Decipher import Decipher
from urllib.parse import unquote
from os import path
from requests import get
from re import findall

class Youtube():
    def __init__(self,url,video:bool,quality:int,audio:bool=False):
        self.url=url
        self.video=video
        self.audio=audio
        self.quality=quality
        self.options = Options()
        self.options.add_argument("--headless")
        self.chrome_driver = r"%userprofile%\Documents\Python Projeler\YoutubeImageDownloader\chromedriver.exe"
        self.driver = webdriver.Chrome(options=self.options,executable_path=self.chrome_driver)
        self.cwd = path.dirname(path.abspath(__file__))
        self.config = load(open(self.cwd+"/config.json", "rb"))
        self.videoData=self.get_video_data(self.url)
        self.streamData=self.videoData["streamingData"]
        self.videoDetails=self.videoData["videoDetails"]
        self.videoTitle=self.videoDetails["title"]
        self.thumbnail="https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(self.videoDetails["videoId"])
        
    
    def get_js(self):
        self.base_data = get('https://youtube.com/watch?v=1').text
        self.js_url = 'https://youtube.com/'+findall(r'"jsUrl":"(.*?)"', self.base_data)[0]
        self.js_file = get(self.js_url).text
        self.data = Decipher(self.js_file, process=True).get_full_function()
        self.config['js'] = self.data
        open(self.cwd+'/config.json', 'w').write(dumps(self.config))
        return self.data
    
    def get_video_data(self,url:str):  
        self.driver.get(url)
        self.source=self.driver.find_element_by_xpath('/html/body/script[1]').get_attribute('innerHTML')
        self.driver.close()
        x=self.source.find("{")
        self.source=self.source[x:]
        x=self.source.find("; var")
        self.source=self.source[:x]
        return self.source
    
    def get_download_url(self):
        pass
    
    def save_download_url(self):
        pass