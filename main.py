## to run, type in command line: $ streamlit run main.py
import resume_analyzer as ra
import streamlit as st
import pprint
import json,operator

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Resume Ranker</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'> This application will analyze submitted resumes against your job posting and recommend the top candidates for your position.", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

#JOB POSTING SUBMISSION
with col1:
    st.markdown("Please upload the job posting.")
    job_posting = st.file_uploader("Upload job posting", accept_multiple_files=False)
    if job_posting:
        st.markdown("File uploaded")
    #display info for file uploaded
        bytes_data = job_posting.read()
        st.write("filename:", job_posting.name)
        with st.expander("click for more info"): 
            st.write(bytes_data)
                

    #save file locally
        save_folder = 'F:/tmp/posting'
        save_path = 'Path(save_folder,job_posting.name)'
        if save_path:
            st.success(f'File {job_posting.name} is successfully saved!')

def gen_response():
    text = extract_job_req(job_posting)
    result = match_resumes('data/resumes', text)
    return result    
        #how do we place these files locally in the pdf folder?
 
#RESUME SUBMISSION"
with col2:
    st.markdown("Please upload the resumes received for your posting.")

    resume_uploaded_files = st.file_uploader("Upload resume file(s)", accept_multiple_files=True)
    if resume_uploaded_files:
        st.markdown("File uploaded")

    #display info for file uploaded
    for uploaded_file in resume_uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        with st.expander("click for more info"): 
            st.write(bytes_data)
            

    #save file locally
        save_folder = '/data/resumes'
        save_path = 'Path(save_folder,uploaded_file.name)'
        if save_path:
            st.success(f'File {uploaded_file.name} is successfully saved!')
        
        #how do we place these files locally in the pdf folder?

        # st.expander(bytes_data)

#OUTPUT and recommendations
with col3:
    analysis_result = ra.gen_response()
    new_result = []

   # sorted_result = sorted(analysis_result, key=lambda x:x['Total score'], reverse=True)
   # analysis_result.sort(key=operator.itemgetter('Total score'))
    #st.write(json.dumps(analysis_result, indent=2))

    for i in analysis_result:
        new_result.append(i['text'])
        st.write(i['text']['Name of the candidate'])
        st.write(i['text']['Total score'])
    print(new_result)
    
#     sorted_result = sorted(new_result, key=lambda x:x['Total score'], reverse=True)
#     for i in sorted_result:
#         st.write(i)
# #