import boto3
import pandas as pd

def load(path, secret_key):
    s3 = boto3.client('s3', aws_access_key_id='AKIAV7R5INR7VARWYT7K', aws_secret_access_key=secret_key)
    read_file = s3.get_object(Bucket = 'nodeflux-intern-ai',Key = path)
    df = pd.read_csv(read_file['Body'])
    return df

def save(df_update, path, secret_key):
    s3 = boto3.client('s3', aws_access_key_id='AKIAV7R5INR7VARWYT7K', aws_secret_access_key=secret_key)
    appended_data = df_update.to_csv(None, index=False).encode()
    s3.put_object(Body=appended_data, Bucket = 'nodeflux-intern-ai',Key = path)
    return