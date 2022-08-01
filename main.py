from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
from source.models.resume import StudentModel
from source.apis.file_upload import router
app = FastAPI()
app.include_router(router)
