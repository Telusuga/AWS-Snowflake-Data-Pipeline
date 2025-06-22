import json
import io
import boto3
import zipfile

def lambda_handler(event, context):
    s3=boto3.client('s3')
    glue=boto3.client('glue')
    bucket='lambda-extract-test'
    source_path='zipped/'
    response = s3.list_objects_v2(Bucket=bucket, Prefix=source_path)
    files=[]
    for obj in response.get('Contents', []):
        #print(obj['Key'])
        #print(obj['Key'].split('/')[1])
        #print(type(obj['Key'].split('/')[1]))
        files.append(obj['Key'].split('/')[1])
    print(files)
    print(files[0])
    try:
        if(files[0].split('.')[1]=='zip'):
            print("Zip file found")
            zip_key=source_path+files[0]
            response = s3.get_object(Bucket=bucket, Key=zip_key)
            zip_content = response['Body'].read()
            with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_ref:
                count=0
                for i in zip_ref.namelist():
                    count+=1
                for file_name in zip_ref.namelist():
                    print(f"Extracting: {file_name}")
                    extracted_file = zip_ref.read(file_name)
                    try:
                        s3.put_object(Bucket=bucket, Key=f'unzipped/movie_data/{file_name}', Body=extracted_file)
                    except Exception as e:
                        return {
                            'statusCode': 500,
                            'body': json.dumps(e)
                                }
                if(count==len(zip_ref.namelist())):
                    response = glue.start_job_run(JobName='Snowflake JOB')
                    print("Job started with run ID:", response['JobRunId'])
                    return {
                        'statusCode': 200,
                        'body': json.dumps('Data load is successful')
                            }
                else:
                    print("Number of files extracted is having mis-match")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
        'statusCode': 500,
        'body': json.dumps(f'There is an issue: {str(e)}')
        }


    
    #print(zip_content)
    


    
