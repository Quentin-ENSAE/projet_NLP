import os
import s3fs
import pandas as pd

# Create filesystem object
S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

BUCKET_OUT = "s3://quentin1999/Data_Projet_NLP"
FILE_KEY_OUT_S3 = "data/df_final"
FILE_PATH_OUT_S3 = BUCKET_OUT + "/" + FILE_KEY_OUT_S3

df_final = pd.read_parquet('data/df_final')

with fs.open(FILE_PATH_OUT_S3, 'w') as file_out:
    df_final.to_csv(file_out)