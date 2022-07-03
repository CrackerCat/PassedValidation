from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from geetest.GeetestFour import GeetestFour
from geetest.GeetestThree import GeetestThree

geetest_router = APIRouter(prefix='/geetest', tags=['极验'])


@geetest_router.get('/v3/{gt}/{challenge}', response_class=ORJSONResponse, summary='极验3代校验,支持无感，滑块，文字点选')
def v3_verify(gt: str, challenge: str, referer: str = None):
    """
    极验3代校验
    :param gt:
    :param challenge:
    :param referer:
    :return:
    """
    validate, validation_type = GeetestThree(gt, challenge, referer).validation()
    return {
        'success': True,
        'validation': validate,
        'type': validation_type
    }


@geetest_router.get('/v4/{captcha_id}', response_class=ORJSONResponse, summary='极验4代校验,支持无感，滑块，文字点选')
def v4_verify(captcha_id: str):
    """
    极验4代校验
    :param captcha_id:
    :return:
    """
    captcha_type, captcha_id, lot_number, captcha_output, gen_time, pass_token = GeetestFour(captcha_id).validation()
    return {
        'success': True,
        'data': {
            "captcha_id": captcha_id,
            "lot_number": lot_number,
            "captcha_output": captcha_output,
            "gen_time": gen_time,
            "pass_token": pass_token
        },
        'type': captcha_type
    }
