import fileinput
from fastapi import  File, UploadFile
from source.models.resume import StudentModel
from fastapi import APIRouter
from source.services.resume import resumeUtility
import pandas as pd
from source.services.maching import prepare,final_result
router = APIRouter(prefix="/resumes")


@router.post("/", response_description="Add new resume", response_model=StudentModel)
async def upload_resume(resume: UploadFile = File(...)):
    return await resumeUtility.add_resume(resume)
router_job = APIRouter(prefix="/jobs")

@router_job.post("/")
async def prepare_data():
    await prepare()

@router_job.get("/")
async def get_top_resumes(id:str):
    return {"resumes_ids": await final_result(id)}

"""@router.post("", response_model=Resume)
async def upload_resume(resume: UploadFile = File(...)):
    return await resumeUtility.add_resume(resume)"""
