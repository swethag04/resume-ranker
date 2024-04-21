import os
from getpass import getpass
import glob
import PyPDF2

OPENAI_API_KEY = getpass()
os.environ["OPENAI_API_KEY"]  = OPENAI_API_KEY

from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def summarize_resumes(pdf_folder):
    
    summaries = []
    for pdf_file in glob.glob(pdf_folder + "/*.pdf"):
        loader = PyPDFLoader(pdf_file) 
        documents = loader.load()
    
        # Define prompt
        prompt_template = """Write a concise summary of the following resume: Include name, title, years of experience,
        most recent role, past employers, achievements and skills"
         "{text}"
        CONCISE SUMMARY:"""
        prompt = PromptTemplate.from_template(prompt_template)

        # Define LLM chain
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        # Define StuffDocumentsChain
        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
        summary = stuff_chain.run(documents)
       # print("Summary for: ", pdf_file)
       # print(summary)
       # print("\n")
        summaries.append(summary)
        
    return summaries


def extract_job_req(job_desc):
    job_loader = PyPDFLoader('data/software-engg-manager-job-description.pdf') 
    desc = job_loader.load()
    prompt_template = """
            You are an expert extraction algorithm. 
            Extract the key qualifications required for this role from the job description 
            in JSON format.
            The keys in the JSON are job title, experience, technical skills, social 
            skills, degree.                       
        "{text}"
        OUTPUT: """
    prompt = PromptTemplate.from_template(prompt_template)
   
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    job_desc_json = llm_chain.invoke(desc)
    return job_desc_json

def match_resumes(pdf_folder, job_desc_json):
    # Define prompt
        prompt_template = """ 
        You are an expert recruiter specializing in  analyzing job descriptions and 
        matching resumes. Your role involves a meticulous process of evaluating resumes 
        against specific job requirements.

        You are provided with resumes of multiple candidates  {text}

        You are also provided with  description for the job being hired {job_desc_json}

        Review the job description noting job title, experience, technical skills, social 
        skills, degree required for the job. Each category is scored on a scale of 1 to 5, 
        where 1 indicates a poor match and 5 indicates an excellent match.

        Before assigning scores, take a moment to reflect on the candidate's overall profile 
        in relation to the job description. Evaluate the candidate's work history for relevance 
        to the job's experience requirements, considering past roles, industries, and levels of 
        responsibility. Assess how the candidate's listed skills align with the job's requirements, 
        including both hard and soft skills

        Sum the scores to get a total that indicates the match level between the candidate's resume 
        and the job description

        Rank all the resumes in descending order of scores and show only the top 2 matching candidates.
        
        Final output should be generated in the below format as a JSON with the below keys:
         
         'Name of the candidate': 
         'Title':
         'Current Employer':
         'Score for job title':
         'Score for experience':
         'Score for social skills':
         'Score for technical skills':
         'Score for degree':
         'Total score':
         """
        prompt = PromptTemplate.from_template(prompt_template)
        responses=[]
        for pdf_file in glob.glob(pdf_folder + "/*.pdf"):
            loader = PyPDFLoader(pdf_file) 
            documents = loader.load()
            # Define LLM chain
            llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
            llm_chain = LLMChain(llm=llm, prompt=prompt)
            response = llm_chain.invoke({'text':documents, 'job_desc_json':job_desc_json})
            responses.append(response)
        return(responses)

 
text = extract_job_req('data/software-engg-manager-job-description.pdf')
result = match_resumes('data/resumes', text)

for i in result:
     print(i['text'])

