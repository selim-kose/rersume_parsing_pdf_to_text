#!/usr/bin/env python
# coding: utf-8

# In[36]:


import spacy #nlp
import pdfminer #pdf2tx
import re #regex
import os #file manip
import pandas as pd #csv - tabular


# In[37]:


import pdf2txt


# # converting pdf to txt

# In[39]:


def convert_pdf(f):

    output_filename = os.path.basename(os.path.splitext(f)[0]) + ".txt"
    output_filepath = os.path.join("output/txt/", output_filename)
    pdf2txt.main(args=[f, "--outfile", output_filepath]) #pdf to txt and save it in the given location
    print(output_filepath + " saved successfully!!!")
    return open(output_filepath).read()


# # load the language model

# In[41]:


nlp = spacy.load("en_core_web_sm")


# In[43]:


result_dict = {'name': [], 'phone': [], 'email': [], 'skills': []} 
names = []
phones = []
emails = []
skills = []


# In[44]:


def parse_content(text):
    skillset = re.compile("python|java|sql|hadoop|tableau")
    phone_num = re.compile(r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}')
    doc = nlp(text)
    name = [entity.text for entity in doc.ents if entity.label_ == "PERSON"][0].strip()
    print(name)
    email = [word for word in doc if word.like_email == True][0]
    print(email)
    phone = str(re.findall(phone_num, text.lower()))
    skills_list = re.findall(skillset, text.lower())
    unique_skills_list = str(set(skills_list))
    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print("Extraction completed successfully!!!")


# In[45]:


for file in os.listdir('resumes/'):
    if file.endswith('.pdf'):
        print('Reading.....' + file)
        txt = convert_pdf(os.path.join('resumes/',file))
        parse_content(txt)


# In[46]:


result_dict['name'] = names
result_dict['phone'] = phones
result_dict['email'] = emails
result_dict['skills'] = skills
print(result_dict)


# In[47]:


result_df = pd.DataFrame(result_dict)
result_df


# In[35]:


result_df.to_csv('output/csv/parsed_resumes.csv')

