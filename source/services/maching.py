from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from pandas.io.json import json_normalize
import numpy as np
import pandas as pd
import ast
from source.models.job_description import JobDescriptionModel
from fastapi.encoders import jsonable_encoder
from source.db_helpers.db_connection import db
"""class maching:
    def __init__(self, labels, resumes, DataJobs, Skills):
        self.labels = labels
        self.resumes = resumes
        self.DataJobs = DataJobs
        self.Skills = Skills"""

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
async def prepare():
        dataJobs= pd.read_csv('DataJobs.csv')
        dataJobs = dataJobs.drop(labels='Unnamed: 0', axis=1)

        for i in range(0, len(dataJobs['skills'])):
                dataJobs['skills'][i] = ast.literal_eval(dataJobs['skills'][i])
                dataJobs['Degrees'][i] = ast.literal_eval(dataJobs['Degrees'][i])
                dataJobs['Majors'][i] = ast.literal_eval(dataJobs['Majors'][i])
                dataJobs['Degree years of experience'][i] = ast.literal_eval(dataJobs['Degree years of experience'][i])
        for index, row in dataJobs.iterrows():
         job_description = JobDescriptionModel(job_title=row['Job Title'], skills=row['skills'],
                                              degrees=row['Degrees'], majors=row['Majors'],
                                              experience=row['years of experience in skills'],
                                              education=row['Degree years of experience'])
         job_description = jsonable_encoder(job_description)
         new_job_description = await db["job_description"].insert_one(job_description)
         created_job_description = await db["job_description"].find_one({"_id": new_job_description.inserted_id})


from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pprint import pprint
def Similarity_HF(s1,s2): #s1 for the job && s2 for the resume /SKILLS
  k=0
  h=0
  l=1
  M1=[]
  M2=[]

  print('s1',s1)
  if sorted(s1) == sorted(s2) :
    s1=[]
    h=len(s2)
  elif s1==[] or s2==[]:
    h=1
  else:
   for a in s1:
    for b in s2:
      if a==b and (len(s1)>len(s2)):
        s1.remove(a)
        M1.append(a)
        h=h+1
      elif a==b and (len(s1)<=len(s2)):
        s2.remove(a)
        M2.append(a)
        h=h+1
  sentences=s1+s2
  print("sent",sentences)
  sentence_embeddings=model.encode(sentences)
  print("sent-embed",sentence_embeddings)
  for i in range(len(s2)):
    for j in range(len(s2),len(sentences)):
      k=k+cosine_similarity(sentence_embeddings[i].reshape(1,-1), sentence_embeddings[j].reshape(1, -1))[0][0]
      l=l+1
  k=k/l
  print('I am here cosine')
  if k==0:
    k=(h+k)/h
  else:
    k=(h+k)/(h+1)
  for i in M1:
    s1.append(i)
  for i in M2:
    s2.append(i)

  return k





def Similarity_D_HF(s1, s2):  # s1 for the job && s2 for the resume
    k = 0
    h = 0
    M = []
    k = 0
    h = 0
    l = 1
    M1 = []
    M2 = []
    sentences = s1 + s2
    if s1 == []:
        return None
    elif s2 == [] and not (s1 == []):
        return -1
    else:
        if sorted(s1) == sorted(s2):
            s1 = []
            h = len(s2)
        else:
            for a in s1:
                for b in s2:
                    if a == b and (len(s1) > len(s2)):
                        s1.remove(a)
                        M1.append(a)
                        h = h + 1
                    elif a == b and (len(s1) <= len(s2)):
                        s2.remove(a)
                        M2.append(a)
                        h = h + 1
        sentences = s1 + s2
        sentence_embeddings = model.encode(sentences)
        for i in range(len(s2)):
            for j in range(len(s2), len(sentences)):
                k = k + cosine_similarity(sentence_embeddings[i].reshape(1, -1), sentence_embeddings[j].reshape(1, -1))[0][
                        0]
                l = l + 1
        k = k / l
        if k == 0:
            k = (h + k) / h
        else:
            k = (h + k) / (h + 1)
        for i in M1:
            s1.append(i)
        for i in M2:
            s2.append(i)
        return k
def build_skills(DataResumes,DataJobs):
  data=[]
  data2=[]
  frame={}
  L=[]
  L2=[]
  for i in range(DataResumes.shape[0]):
      data2.append(Similarity_HF(DataJobs['skills'][0],DataResumes['skills'][i]))
  for z in range(DataResumes.shape[0]):
    L2.append("Resume with skills {}".format(z))
  frame = pd.DataFrame(data2, columns=["Job name {}".format(list(DataJobs['job_title'])[0])] , index=L2)
  print("this is frame",frame)
  return frame

def build_majors(DataResumes,DataJobs):
  data=[]
  data2=[]
  frame2={}
  L=[]
  L2=[]
  for i in range(DataResumes.shape[0]):
      data2.append(Similarity_HF(list(DataJobs['majors'])[0],DataResumes['majors'][i]))
  for z in range(DataResumes.shape[0]):
    L2.append("Resume with skills {}".format(z))
  frame2 = pd.DataFrame(data2, columns=["Job name {}".format(list(DataJobs['job_title'])[0])] , index=L2)
  return frame2

def build_degrees(DataResumes,DataJobs):
  data=[]
  data2=[]
  frame3={}
  L=[]
  L2=[]
  for i in range(DataResumes.shape[0]):
      data2.append(Similarity_HF(list(DataJobs['degrees'])[0],DataResumes['degrees'][i]))
  for z in range(DataResumes.shape[0]):
    L2.append("Resume with skills {}".format(z))
  frame3 = pd.DataFrame(data2, columns=["Job name {}".format(list(DataJobs['job_title'])[0])] , index=L2)
  return frame3


async def similarity_total(DataJobs,DataResumes):


 frame_skills=build_skills(DataResumes,DataJobs)
 frame_degrees=build_degrees(DataResumes,DataJobs)
 frame_majors=build_majors(DataResumes,DataJobs)
 Data_test=frame_skills
 for j in range(3):
     Data_test["Job name {}".format(list(DataJobs['job_title'])[0])][j]=0.6*frame_skills["Job name {}".format(list(DataJobs['job_title'])[0])][j]+0.2*frame_degrees["Job name {}".format(list(DataJobs['job_title'])[0])][j]+0.2*frame_majors["Job name {}".format(list(DataJobs['job_title'])[0])][j]
 return Data_test

async def ranking(DataJobs,DataResumes):
  Data_test=await similarity_total(DataJobs,DataResumes)
  for ch in list(Data_test.columns):
    Data_test[ch]=Data_test[ch].rank()
  return Data_test
async def set_ids(id): #adding the ids d resumes
  data_job = await db["job_description"].find_one({"_id": id})
  data_resumes = await db["resumes"].find().to_list(1000)
  DataJobs = json_normalize([data_job])
  DataResumes = json_normalize(data_resumes)
  print('columnsssssssss',DataJobs.columns)
  Data_test=await ranking(DataJobs,DataResumes)
  L=[]
  for i in range(len(DataResumes['_id'])):
    L.append(DataResumes['_id'][i])
    print("L",L)
  Data_test.insert(loc=0,
          column='ids',
          value=L)
  print(Data_test)
  return Data_test
#THIS IS OUR FUNCTION
async def final_result(id):
  Data_test=await set_ids(id)
  k=""
  L=[]
  for i in Data_test.columns:
    k=i
  for i in range(Data_test.shape[0]):
    if Data_test[k][i]==1.0 or Data_test[k][i]==2.0 or Data_test[k][i]==3.0:
      L.append(Data_test['ids'][i])
  return L