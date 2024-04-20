import os
from getpass import getpass
import glob

OPENAI_API_KEY = getpass()
os.environ["OPENAI_API_KEY"]  = OPENAI_API_KEY

 
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate


def summarize_resumes(pdf_folder):
    summaries = []
    for pdf_file in glob.glob(pdf_folder + "/*.pdf"):
        loader = PyPDFLoader(pdf_file) 
        documents = loader.load()
    
        # Define prompt
        prompt_template = """Write a concise summary of the following resume: Include name, title, years of experience,
        most recent role, past employers, achievements"
         "{text}"
        CONCISE SUMMARY:"""
        prompt = PromptTemplate.from_template(prompt_template)

        # Define LLM chain
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        # Define StuffDocumentsChain
        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
        summary = stuff_chain.run(documents)
        print("Summary for: ", pdf_file)
        print(summary)
        print("\n")
        summaries.append(summary)

        
    return summaries

summarize_resumes("data/resumes")


