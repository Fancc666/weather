import requests
import schedule
import time
import re
from pathlib import Path
import os

config = {
    # seconds
    "interval": int(os.getenv("INTERVAL", "3600")),
    # data folder
    "folder": Path(__file__).parent / os.getenv("FOLDER", "data"),
    "base": os.getenv("BASE", "http://m.nmc.cn/publish/observations/hourly-precipitation.html")
}

# retry decorator
def retry(times=3, interval=2):
    def deco(func):
        def newfunc(*args, **kwargs):
            for i in range(times+1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print("[ERROR]\n"+str(e))
                    if i != times:
                        print(f"Retrying {i+1}/{times}, waiting for {interval} seconds...")
                    else:
                        raise e
                time.sleep(interval)
        return newfunc
    return deco

class Weather:
    def __init__(self) -> None:
        self.session = requests.session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
        })
    def get(self):
        print("\n" + "*" * 40)
        print("RUNNING AT", fmtDate())
        url = self.find_img_url()
        if url is None:
            print("no image found, cycle skipped")
        else:
            self.save_img(url)
        print("NEXT RUN AT", fmtDate(config["interval"]))
    @retry()
    def find_img_url(self):
        print("getting image url")
        response = self.session.get(config["base"])
        response.encoding = "utf-8"
        # print(response.text)
        imgUrls = re.findall(r'data-src="(https://image\.nmc\.cn/product/.*?)"', response.text)
        if len(imgUrls) == 0:
            print("no image found")
            return None
        print(imgUrls[-1])
        return imgUrls[-1]
    @retry()
    def save_img(self, url):
        data = self.session.get(url)
        imgName = fmtDate()+".jpg"
        with open(config["folder"] / imgName, "wb") as f:
            f.write(data.content)
        print(imgName, "saved succesfully")

def fmtDate(delay=0):
    timeStamp = time.time()
    timeArr = time.localtime(timeStamp + delay)
    timeStr = time.strftime("%Y%m%d%H%M%S", timeArr)
    return timeStr

if __name__ == "__main__":
    myWeather = Weather()
    schedule.every(config["interval"]).seconds.do(myWeather.get)
    # run first time immediately
    myWeather.get()
    while True:
        schedule.run_pending()
        time.sleep(1)
