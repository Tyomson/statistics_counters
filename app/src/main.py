from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sentry_sdk

import statistics.router
from config import CONFIG, ErrorDetails

tags_metadata = [
    {
        'name': 'statistics',
        'description': 'Working with the statistics directory'
    },
]

sentry_sdk.init(
    CONFIG['sentry_url'],
    traces_sample_rate=1.0
)


app = FastAPI(
    title='Statistics Counters',
    description='API for working with the statistics directory!',
    version='0.0.1',
    openapi_tags=tags_metadata,
)
# base.Base.metadata.create_all(bind=base.engine)

app.include_router(statistics.router.router)

app.add_middleware(
    CORSMiddleware,
)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    try:
        code = ErrorDetails.codes[exc.detail]
    except KeyError:
        code = exc.status_code
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': {
                'code': code,
                'detail': exc.detail
            }
        }
    )
