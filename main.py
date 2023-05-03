import streamlit as st
import pandas as pd
from difflib import SequenceMatcher

st.set_page_config(page_title='Data Matcher', page_icon=':computer:', layout='wide')
st.title("Assessment Data Matcher")

def find_best_match(name, name_list):
    best_score = 0
    best_match = None
    for n in name_list:
        score = SequenceMatcher(None, name, n).ratio()
        if score > best_score:
            best_score = score
            best_match = n
    if best_score >= 0.9:
        return best_match
    else:
        return None


def per_assessment(pat_file, classlist):
    assessment_df = pd.read_excel(pat_file, header=11)
    students_df = pd.read_excel(classlist)
    listo = []
    for i, row in assessment_df.iterrows():
        student_name = row['Given name'].title() + ' ' + row['Family name'].title()
        matching_names = students_df['First Name'] + ' ' + students_df['Last Name']
        matching_name = find_best_match(student_name, matching_names)

        if matching_name:
            student_info = students_df.loc[matching_names == matching_name].iloc[0]
            assessment_df.loc[i, 'Given name'] = student_info['First Name']
            assessment_df.loc[i, 'Family name'] = student_info['Last Name']
            assessment_df.loc[i, 'DOB'] = student_info['Birth Date']
            assessment_df.loc[i, 'Gender'] = student_info['Gender']
        else:
            listo.append(f'NAME: {student_name}, DOB: {row["DOB"]}, GENDER: {row["Gender"]}')
    if len(listo) == 0:
        return assessment_df
    return listo

st.write("---")

pat_file = st.file_uploader('Upload PAT Files Here', type=None, accept_multiple_files=True, key=None,
                        help=None,
                        on_change=None, args=None,
                        kwargs=None, disabled=False, label_visibility="visible")

classlist = st.file_uploader('Upload Classlist here', type=None, accept_multiple_files=False, key=None,
                        help=None,
                        on_change=None, args=None,
                        kwargs=None, disabled=False, label_visibility="visible")

st.write('---')

if pat_file and classlist:
    for files in pat_file:
        result = per_assessment(files, classlist)
        col1, col2, = st.columns(2)
        if type(result) == list:
            with col1:
                st.error(f'Issues with {files.name} detected')
            with col2:
                st.write(result)
        else:
            with col1:
                st.success(f'File {files.name} looks good to go')
            with col2:
                st.download_button(label = files.name, data = result.to_csv().encode('utf-8'), file_name=files.name, use_container_width=True)
        st.write('---')
