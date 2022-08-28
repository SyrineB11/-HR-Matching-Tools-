# resume-parser
# HR-Matching-Tools

# Problem Overview

The Process of selecting the best resumes manually showed many drawbacks
such as being Time-consuming, getting Slower responses, Ineffective/Non-persistent data,
Inproductivity within the HR team. 

Besides, the traditional way that recruiters are using to select candidates doesn't take into consideration all important details. Recruiters have to screen all the applications manually and then calculate the similarity in an efficient way.

As a solution in this project, we calculated the similarity between the resume and the job description and then return the resumes with the highest similarity score.


## I - Data Preparation
I-1 ResumesDataset  **resume-parser**

II-2 JobsDataset 

To build the JobsDataset we used a costumized NER system to extract the Skills, Degrees and Majors from the kaggle's JobsDescriptions, 
then we created the  years of experience in skills and  Degree years of experience features using both NER system and RegEx explained as following :

   - kaggle (https://www.kaggle.com/datasets/nikhilbhathi/data-scientist-salary-us-glassdoor) 
       > JobDescription 
       
       >  Job Title
       
   ![Job categories](https://user-images.githubusercontent.com/78451998/185714017-5e7e9486-1e37-4ca6-9c6b-344cd2418192.png)
   
   - NER + (3 json files) [SKILLS , DEGREES ,MAJORS ]
     
     +  Sample (using SKILLS jsonfile)
     
   
   ![sample_skills](https://user-images.githubusercontent.com/78451998/185714002-7d8c439f-d5f2-4754-a925-183eafaff816.png)
   
   
   + RegEX to extract the JOBS dataset
   
![Datajob Dataset](https://user-images.githubusercontent.com/78451998/185712634-4b57b166-964d-4169-a644-2f52158ef10b.png)


## II- STS

## - Definitions 

1- STS : SEMANTIC TEXTUAL SIMILARITY (comparison of sentence pairs)

2- Transfer Learning

3- Word embeddings
 - Count Vectorizer
 - Word2vec
 
4- Sentence embedding
 - Bag of words
5- LSTM (Optional)

6- BERT for STS tasks
  > SBERT and Sentence Transformers
    > DistilBERT
    
7- Cross-Encoders

8- Dense embeddings (SBERT,GTP-3) vs Sparse embeddings(TF-IDF)

9- Cosine similarity

![cosine](https://user-images.githubusercontent.com/78451998/186685650-bf5b36a3-c8fa-48f3-8e51-8aa2e9287639.png)



## - Methodology

### EXTRACTING THE BEST MODEL FOR WORD SIMILIARITY

1- WMD (Word Mover’s Distance for Text Similarity) THE CLOSER TO ZERO THE MORE SIMILAR

![WMD](https://user-images.githubusercontent.com/78451998/186677693-b9a1752b-d39a-4488-a82e-5f296a85586e.png)





2-  Dense embeddings using Sentence Transformers (approved for semantic search/similarity):
 
   - SBERT(sentence BERT)
   
         - model : paraphrase-MiniLM-L6-v2 (It maps sentences & paragraphs to a 384 dimensional dense vector space )
         
      ![paraphrase-MiniLM-L6-v2](https://user-images.githubusercontent.com/78451998/185649175-68ce7fd6-a7f5-40d1-ae91-680d381500ae.png)
      
      ![paraphrase-MiniLM-L6-v2 2png](https://user-images.githubusercontent.com/78451998/185746344-4902db9b-db98-49f0-9280-c7900b7c1c2d.png)


         
         
         - model : all-MiniLM-L12-v1
         
      ![paraphrase-MiniLM-L12-v2](https://user-images.githubusercontent.com/78451998/185649219-78e1a249-ff8c-417a-9106-b6798da663c6.png)
      
      ![L12-2](https://user-images.githubusercontent.com/78451998/185747269-2ee2a0e1-1b49-400b-ab43-31651297ca21.png)

         
         - model : all-mpnet-base-v2 ( It maps sentences & paragraphs to a 768 dimensional dense vector space )
      ![all-mpnet-base-v2](https://user-images.githubusercontent.com/78451998/185654620-46767d43-3bee-4c4f-9184-ca4d0d6d09cc.png)
      
      ![all-mpnet-base-v2 2](https://user-images.githubusercontent.com/78451998/185749893-38004557-2c88-4480-a514-e31d2c35f023.png)

         
         - model : all-roberta-large-v1 (maps sentences & paragraphs to a 1024 dimensional dense vector space)
         
     ![all-roberta-large-v1](https://user-images.githubusercontent.com/78451998/185653297-8110eb9e-77b6-40c2-b869-d67ac4c681fd.png)
     
     ![all-roberta-large-v1 2](https://user-images.githubusercontent.com/78451998/185750700-113a22b5-3c07-4e01-ac5f-654497bf68b5.png)
 
         
         - model : bert-base-nli-mean-tokens( maps sentences & paragraphs to a 768 dimensional dense vector space )
     ![bert-base-nli-mean-tokens](https://user-images.githubusercontent.com/78451998/185658202-b254e9c4-e299-4d8b-a154-da9782ea7a6f.png)
     
     ![Bert-base](https://user-images.githubusercontent.com/78451998/185753890-5762a6a3-393d-4bba-bdd8-00bf4aae0ba0.png)
          
         - msmarco-distilbert-cos-v5   (It maps sentences & paragraphs to a 768 dimensional dense vector space and was designed for semantic search. It has been trained on 500k (query, answer) pairs from the MS MARCO Passages dataset)
          
        ![msmarco-distilbert-cos-v5](https://user-images.githubusercontent.com/78451998/185739187-7cc297a2-5177-43ba-9039-ba3699c20c22.png)
        
        ![masmarco-sentence](https://user-images.githubusercontent.com/78451998/185792262-7f5eb60d-306b-403e-8c1c-9175ff5236d4.png)


         
       - DistilBERT  (a distilled version of BERT): 
         
          
          - quora-distilbert-base ( It maps sentences & paragraphs to a 768 dimensional dense vector space )
     ![quora-distilbert-base](https://user-images.githubusercontent.com/78451998/185706963-a26895d9-769c-4502-a86a-052c3f343007.png)
     
        ![quora distilbert](https://user-images.githubusercontent.com/78451998/185754302-87242af1-cae8-412a-9e6c-d614c03f9272.png)

     
      - Cross Encoder (Cross-Encoders can be used whenever you have a pre-defined set of sentence pairs you want to score. For example, you have 100 sentence pairs and you want to get similarity scores for these 100 pairs.):
       
         - model : stsb-roberta-large (This model was trained using SentenceTransformers Cross-Encoder class 
         // his model was trained on the STS benchmark dataset. The model will predict a score between 0 and 1 how for the semantic similarity of two sentences.)
         
          ![stsb-roberta-large](https://user-images.githubusercontent.com/78451998/185737828-e2e4bd09-4871-4f28-9061-99ee4729d1dc.png)
          
          ![roberta2](https://user-images.githubusercontent.com/78451998/185792033-c612aebd-2fb2-44ed-9b8d-cbdafa31e7ba.png)

           
          
  - GPT-3 (autoregressive models which internally mask the future tokens)
  
  ![GPT-3](https://user-images.githubusercontent.com/78451998/185740633-ad60d2d2-973d-4da5-91c0-954b65b03316.png)
  
  ![GPT-3 2](https://user-images.githubusercontent.com/78451998/185792709-6bb69d6f-ad32-47a3-861c-4e05b54c1a70.png)

 -  SPACY -> model: en_core_web_sm

![en_core_web_sm](https://user-images.githubusercontent.com/78451998/185712371-cf25f567-16c0-4585-9982-94f3c8af7165.png)

![en_core_web_sm_data](https://user-images.githubusercontent.com/78451998/185936446-0d60b82d-4bb1-42fc-ac6b-18f3b595c402.png)
![okay](https://user-images.githubusercontent.com/78451998/185939131-2e4281c6-b328-4135-ba2d-3fe45889b26e.png)



- Job
    
  ```
    ['engineering','business','data analysis','database','computer science','artificial intelligence','ai', 'bi','tableau','python','matlab','data visualization','communication','algorithm', 'machine learning','data mining','anomaly detection', 'training']
     ```

3- First Evaluation using these examples :

- Resumes
   
    ```
     lowest_resume = ["engineering","html","css","angular","react js","mongodb","web development","github","devops","responsive design"]
    
    low_resume = ["marketing","business analysis","fraud detection","excel","forecasting",""]
    
    intermediate_resume = ["engineering","mobile development","flutter","design","mongodb","artificial intelligence","python","data mining"]
    
    high_resume = ["mongodb","computer science","engineering","business","data analysis","artificial intelligence","tableau","data visualization","sql","machine learning","fraud detection","python"]

    high_plus_resume = ["mongodb","computer science","engineering","business","data analysis","artificial intelligence","tableau","data visualization","sql","machine learning","fraud detection","python","public speaking","marketing","deployment","github","tensorflow"]
   
    ```
  
4- Second Evaluation using these examples of resumes:
```
lowest_resume_2 = ["html",'php','github',"mongodb","dev","excel","data management","mongodb"]

low_resume_2=["marketing",'html','php','github','web',"excel","management"]

intermediate_resume_2=["web",'php',"python","css","data","html"]

high_resume_2=["mongodb","computer science","data visualization","tableau","anomaly detection","python","ai","matlab"]

high_plus_resume_2=["business","mongodb","tableau","ai","computer science","data analysis","artificial intelligence","data visualisation","data mining","algorithm","java","matlab"]


```
![yepp](https://user-images.githubusercontent.com/78451998/186676533-976b8bee-eedd-4a01-95e4-5107d6d24db1.png)

### Then we chose the SBERT model :   all-mpnet-base-v2 

GOT TOP 4 BEST RESUMES FOR EACH JOB BASED ON THEIR CALCULATED SIMILARITIES 
for each feature we attributed weights to calculate the similarity between all features giving (w1:skills,w2:majors,w3:degrees)

![TOP4](https://user-images.githubusercontent.com/78451998/186678778-a780ca4d-7785-4b77-8cc2-7f97f5ee938a.png)
