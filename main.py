from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from requests import Request

from api.geetest_api import geetest_router
from error.GeetestException import GeetestException

app = FastAPI(title='PassedValidation', description='过验证码校验,目前支持极验3（滑块，文字点选，无感），极验4（滑块，文字点选，无感）'
              , openapi_url='/')

app.include_router(geetest_router)


@app.exception_handler(GeetestException)
async def geetest_exception_handler(_request: Request, exc: GeetestException):
    return ORJSONResponse(status_code=200, content={
        'success': False,
        'error': exc.err_desc
    })


@app.exception_handler(Exception)
async def exception_handler(_request: Request, _exc: Exception):
    return ORJSONResponse(status_code=500, content={'server error'})
