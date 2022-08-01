import fileinput
from fastapi import  File, UploadFile
from source.models.resume import StudentModel
from fastapi import APIRouter
from source.services.resume import resumeUtility

router = APIRouter(prefix="/resumes")


@router.post("/", response_description="Add new resume", response_model=StudentModel)
async def upload_resume(resume: UploadFile = File(...)):
    return await resumeUtility.add_resume(resume)


"""@router.post("", response_model=Resume)
async def upload_resume(resume: UploadFile = File(...)):
    return await resumeUtility.add_resume(resume)"""
