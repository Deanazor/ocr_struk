import boto3
import pandas as pd

def load(key):
    s3 = boto3.client('s3', aws_access_key_id='AKIAV7R5INR7VARWYT7K', aws_secret_access_key='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')
    read_file = s3.get_object(Bucket = 'nodeflux-intern-ai',Key = key)
    df = pd.read_csv(read_file['Body'])
    return df

def save(df_update, key):
    s3 = boto3.client('s3', aws_access_key_id='AKIAV7R5INR7VARWYT7K', aws_secret_access_key='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')
    appended_data = df_update.to_csv(None, index=False).encode()
    s3.put_object(Body=appended_data, Bucket = 'nodeflux-intern-ai',Key = key)
    return