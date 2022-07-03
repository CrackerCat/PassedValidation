import io

import requests
from PIL import Image

slide_ocr = None
word_ocr = None
xy_ocr = None


class OcrUtil:

    @staticmethod
    def get_slide_distance(bg_image: any, slice_image: any, simple: bool = True) -> int:
        """
        获取滑块缺口坐标系位置
        :param simple: 是否是单个滑块图片
        :param bg_image: 背景图片
        :param slice_image: 滑块图片
        :return: 位置
        """
        return 0

    @staticmethod
    def get_word(img: Image.Image) -> list:
        return list()

    @staticmethod
    def get_xy(img: Image.Image) -> dict:
        arr = {}
        return arr
