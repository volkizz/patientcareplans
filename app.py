import streamlit as st
import openai
import boto3

# Set up AWS credentials
ACCESS_KEY = 'AKIA2OMBE47NNS76HSUI'
SECRET_KEY = '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'
BUCKET_NAME = 'bucketformypatients'

s3 = boto3.resource('s3',
                    aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY)

#Connect to GPT3.5 API
openai.api_key = "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"



def load_documents_from_s3(bucket_name):

    documents = []
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        file_content = obj.get()['Body'].read().decode('utf-8')
        document = {
            'title': obj.key,
            'text': file_content
        }
        documents.append(document)
    return documents

documents = str(load_documents_from_s3(BUCKET_NAME))

def main():
    st.title("Patient Care Plans Records AI Helper")

    user_input = st.text_input("User:")

    if user_input:
        response = generate_response(user_input)
        st.write(f"""Slalom AI:
                 """)
        st.write(response)

    uploaded_file = st.file_uploader("Upload Document (txt file)", type="txt")
    if uploaded_file is not None:
        try:
            s3.Bucket(BUCKET_NAME).put_object(Key=uploaded_file.name, Body=uploaded_file)
            st.success("Document uploaded successfully!")
            documents = load_documents_from_s3(BUCKET_NAME)
        except Exception as e:
            st.error(f"""Error uploading document: {str(e)}""")

def generate_response(input_text):
    if input_text is not None:
        with st.spinner('Thinking'):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                temperature = 0,
                messages=[
                    {"role": "system", "content": "You are a medical doctor who creates patients plans"},
                    {"role": "user", "content": input_text + "Use this data" + documents}
                ]
            )
            return response.choices[0].message.content

if __name__ == "__main__":
    main()