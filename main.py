from fastapi import FastAPI
from source.apis.file_upload import router,router_job
app = FastAPI()
app.include_router(router)
app.include_router(router_job)

