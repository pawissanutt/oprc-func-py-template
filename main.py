import logging
import oaas_sdk_py as oaas
import uvicorn
from fastapi import Request, FastAPI, HTTPException
from oaas_sdk_py import OaasInvocationCtx
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
level = logging.getLevelName(LOG_LEVEL)
logging.basicConfig(level=level)


class GreetingHandler(oaas.Handler):
    async def handle(self, ctx: OaasInvocationCtx):
        name = ctx.args.get('name', 'world')
        ctx.resp_body = {"msg": "hello " + name}


app = FastAPI()
router = oaas.Router()
router.register(GreetingHandler())


@app.post('/')
async def handle(request: Request):
    body = await request.json()
    logging.debug("request %s", body)
    resp = await router.handle_task(body)
    logging.debug("completion %s", resp)
    if resp is None:
        raise HTTPException(status_code=404, detail="No handler matched")
    return resp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
