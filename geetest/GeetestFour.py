"""
极验4
"""
import json
import random
import time
import uuid
from io import BytesIO

import requests
from PIL import Image

from error.GeetestException import GeetestException
from geetest import js
from utils.OcrUtil import OcrUtil


class GeetestFour:
    def __init__(self, captcha_id: str):
        self.__captcha_id = captcha_id
        
        self.__static_url = ""
        
        self.__request = requests.session()
        
        self.__request.headers = {
        }
        
        self.__v4_js = js
        
        self.__load_url = ""
        
        self.__verify_url = ""
        
        self.__ocr_util = OcrUtil
        
        self.__load_data = None
        
        self.__lot_number = None
        self.__payload = None
        self.__process_token = None
        self.__payload_protocol = None
        
        self.__captcha_output = None
        self.__gen_time = None
        self.__pass_token = None

    def __load(self):
        """
        加载验证码相关参数请求
        :return:
        """
        callback = f"geetest_{int(time.time() * 1000)}"
        payload = {
            "captcha_id": self.__captcha_id,
            "challenge": uuid.uuid4(),
            "client_type": "web",
            "lang": "zh",
            "risk_type": "ai",
            "callback": callback
        }
        resp_text = self.__request.get(self.__load_url, params=payload).text
        if resp_text.find('error') > -1:
            raise GeetestException(f'error captcha_id:{self.__captcha_id}')
        data = json.loads(resp_text.replace(f"{callback}(", "").replace(")", ""))['data']
        captcha_type = data['captcha_type']
        self.__load_data = data
        self.__lot_number = data['lot_number']
        self.__payload = data["payload"]
        self.__process_token = data["process_token"]
        self.__payload_protocol = data["payload_protocol"]
        self.__datetime = data['pow_detail']['datetime']
        return captcha_type

    @classmethod
    def __get_slide_data(cls, distance):
        """
        生成滑块轨迹
        :param distance: 距离
        :return:
        """
        return []

    def __slide_validation(self):
        """
        滑块校验
        :return:
        """
        bg_url, slice_url = self.__static_url + self.__load_data['bg'], self.__static_url + self.__load_data['slice']
        
        slide_distance = self.__ocr_util.get_slide_distance(bg_url, slice_url, True)
        
        slide_trace_data = self.__get_slide_data(slide_distance)
        
        self.__w = self.__v4_js.call('', slide_trace_data, 0, self.__lot_number, self.__datetime,
                                     self.__captcha_id)
        return self

    def __ai_validation(self):
        
        self.__w = self.__v4_js.call('', self.__captcha_id, self.__lot_number, self.__datetime)
        return self

    def __word_validation(self):
        words = []
        imgs = self.__static_url + self.__load_data['imgs']
        xy_img = Image.open(BytesIO(self.__request.get(imgs).content))
        xys = self.__ocr_util.get_xy(xy_img)
        points = list()
        for word in words:
            if not xys.get(word):
                raise GeetestException('识别文字失败，请重试')
            x, y = xys[word]
            x = x
            y = y
            points.append([x, y])
        pass_time = random.randint(1000, 10000)
        self.__w = self.__v4_js.call("", self.__captcha_id, self.__lot_number, self.__datetime, points,
                                     pass_time)
        return self

    def __verify(self):
        callback = f"geetest_{int(time.time() * 1000)}"
        payload = {
            "captcha_id": self.__captcha_id,
            "client_type": "web",
            "lot_number": self.__lot_number,
            "payload": self.__payload,
            "process_token": self.__process_token,
            "payload_protocol": self.__payload_protocol,
            "pt": 1,
            "w": self.__w,
            "callback": callback
        }
        resp_text = self.__request.get(self.__verify_url, params=payload).text
        if resp_text.find('error') > -1:
            raise GeetestException('verify fail,please again')
        data = json.loads(resp_text.replace(f"{callback}(", "").replace(")", ""))['data']
        self.__captcha_output, self.__gen_time, self.__pass_token = data['seccode']['captcha_output'], data['seccode'][
            'gen_time'], data['seccode']['pass_token']

    def validation(self):
        """
        校验入口
        :return:
        """
        captcha_type = self.__load()
        if captcha_type == 'slide':
            
            self.__slide_validation().__verify()
        elif captcha_type == 'ai':
            
            self.__ai_validation().__verify()
        elif captcha_type == 'word':
            self.__word_validation().__verify()
        else:
            raise GeetestException(f"不支持的类型：{captcha_type}")
        return captcha_type, self.__captcha_id, self.__lot_number, self.__captcha_output, self.__gen_time, self.__pass_token
