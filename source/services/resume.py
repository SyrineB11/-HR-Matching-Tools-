from fastapi import UploadFile
from source.handlers.convert_handler import get_text
from fastapi import Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from source.db_helpers.db_connection import db

S3_BUCKET_NAME = "test-resumes-101"


class CRUDResume():
    async def add_resume(self, resume: UploadFile):
        uploaded_file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{resume.filename}"
        extention = resume.filename.split(".")[-1]
        print(extention)
        file_location = "/app/source/resumes/103" +'.'+extention
        with open(file_location, "wb+") as file_object:
            file_object.write(resume.file.read())
        (email,phone,linkedin,github,skills)=get_text(file_location)
        resume={
            "contact":{
                "email": email if email else '',
                "phone": phone if phone else '',
                "linkedin": linkedin if linkedin else '',
                "github": github if github else ''
            },
            "skills":skills
        }
        resume = jsonable_encoder(resume)
        new_resume = await db["resumes"].insert_one(resume)
        created_student = await db["resumes"].find_one({"_id": new_resume.inserted_id})
        return created_student
            
            
            
                

"""    async def get_resumes(self):
        query = resumes.select()
        return await database.fetch_all(query)

    async def delete_resume(self, id):
        delete = resumes.delete().where(resumes.c.id == id)
        engine.execute(delete)"""


resumeUtility = CRUDResume()
