import json
import boto3
import zipfile
import io

def lambda_handler(event, context):
    # TODO implement
    s3=boto3.client('s3')
    response = s3.list_objects_v2(Bucket='lambda-extract-test', Prefix='raw/')
    files=[]
    for obj in response.get('Contents', []):
        #print(obj['Key'])
        #print(obj['Key'].split('/')[1])
        #print(type(obj['Key'].split('/')[1]))
        files.append(obj['Key'].split('/')[1])
    print(files)
    zip_buffer = io.BytesIO()
    for i in files:
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            content=s3.get_object(Bucket='lambda-extract-test', Key='raw/'+i)['Body'].read()
            zip_file.writestr(i, content)
      # Reset buffer position
    zip_buffer.seek(0)
    
    # Upload the zip back to S3
    s3.put_object(
        Bucket='lambda-extract-test',
        Key='zipped/selected_files.zip',
        Body=zip_buffer.getvalue()
    )
    print('Data Load Successful')
    
    

    return {
        'statusCode': 200,
        'body': json.dumps('Zipping had been completed successfully')
    }
