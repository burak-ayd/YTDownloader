from msilib.schema import Class
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from json import load, dumps
from Decipher import Decipher
from urllib.parse import unquote
from os import path
from requests import get
from re import findall
import math

class Youtube():
    def __init__(self,url,video:bool,quality:int,audio:bool=False):
        self.url=url
        self.video=video
        self.audio=audio
        self.quality=quality
        self.cwd = path.dirname(path.abspath(__file__))
        self.options = Options()
        self.options.add_argument("--headless")
        self.chrome_driver = self.cwd+r"\SeleniumDriver\chromedriver.exe" # Driver Version: 99.0.4844.51
        self.driver = webdriver.Chrome(options=self.options,executable_path=self.chrome_driver)
        self.config = load(open(self.cwd+"/config.json", "rb"))
        self.videoData=self.get_video_data(self.url)
        self.streamData=self.videoData["streamingData"]
        self.videoDetails=self.videoData["videoDetails"]
        self.videoTitle=self.videoDetails["title"]
        self.thumbnail="https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(self.videoDetails["videoId"])
        self.foundLink={"FoundLink":{}}
    
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
        for format in self.streamData["adaptiveFormats"]:
            itag = format["itag"]
            if((itag==137 or itag==136 or itag==299 or itag==135) or (itag==140 or itag==141)):
                if 'signatureCipher' in format.keys():
                    signature, url = format["signatureCipher"].split('&sp=sig&url=')
                    signature = signature.replace("s=",'',1).replace('%253D', '%3D').replace('%3D', '=')
                    deciphered_signature = Decipher().deciphered_signature(
                        signature, algo_js=self.config['js']
                        )
                    url = unquote(url)+'&sig='+deciphered_signature
                    
                    js_passed = False
                    if js_passed is False:
                        try:
                            if get(url, timeout=4, i=True).status_code != 200:
                                self.get_js()
                                deciphered_signature = Decipher().deciphered_signature(signature, algo_js=self.config['js'])
                                url = unquote(url)+'&sig=' + deciphered_signature
                        except Exception:
                            self.get_js()
                            deciphered_signature = Decipher().deciphered_signature(signature, algo_js=self.config['js'])
                            url = unquote(url)+'&sig=' + deciphered_signature
                        js_passed = True
                else:
                    url = format["url"].replace('\\u0026', '&')
                try:
                    quality = format["qualityLabel"]
                except Exception:
                    quality = format["quality"]
                try:
                    size = format["contentLength"]
                except Exception:
                    size = 0
                self.foundLink["FoundLink"].update({"quality":quality,"title":self.videoTitle,"url":url,"size":self.convert_size(size),"thumbnail":self.thumbnail})
        self.save_download_url()

    
    def save_download_url(self):
        ths = open("foundLink.json", "w")
        ths.write(self.foundLink)
        ths.close()
    
    def convert_size(self,size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])