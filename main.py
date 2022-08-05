from fastapi import FastAPI
from source.apis.file_upload import router
app = FastAPI()
app.include_router(router)
