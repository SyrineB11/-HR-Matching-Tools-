from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
from source.models.resume import StudentModel

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mayssa:mayssa@mongodb")
db = client.extaction
