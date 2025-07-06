import airflow
from airflow import DAG
from airflow.providers.amazon.aws.operators.lambda_function import LambdaInvokeFunctionOperator
from datetime import datetime as dt
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.empty import EmptyOperator


dag=DAG(
    dag_id='<Dag_Name>',
    start_date=dt.now(), 
    schedule='@daily',
    catchup=False
)


Lambda_Trigger=LambdaInvokeFunctionOperator(
    task_id='lambda_trigger',
    function_name='<Lambda Funtion Name>',
    aws_conn_id="aws_conn", #Airflow connection ID
    invocation_type="Event", #To enable event based triggering
    log_type='None', #To enable no log is returned upon trigger
    region_name='<The location in which the function is located>', 
    dag=dag
)

wait_for_raw_file = S3KeySensor(
    task_id='wait_for_raw_s3_file',
    bucket_key='<Raw File S3 location>',   # or 'data/input/*.csv'
    bucket_name='<Raw File Source Bucket>',
    aws_conn_id='aws_conn',
    poke_interval=30,
    timeout=600,
)


tranformation=GlueJobOperator(
    task_id='Glue_trigger',
    job_name='<job_name>',
    script_location='<S3 location>',
    s3_bucket='<temp location for processing data>',
    region_name='<The location in which the function is located>',
    aws_conn_id="aws_conn",
    dag=dag
)


wait_for_processed_file = S3KeySensor(
    task_id='processed_file_check',
    bucket_key='<Final_object_location in S3>',   # or 'data/input/*.csv'
    bucket_name='<Destination_bucket>',
    aws_conn_id='aws_conn', #Airflow connection ID
    poke_interval=30, #The time for which airflow checks the bucket
    timeout=600, #Max Timeout interval in seconds
    )


start=EmptyOperator(
    task_id='start',
    dag=dag
)

end=EmptyOperator(
    task_id='end',
    dag=dag
)



start >> Lambda_Trigger >> wait_for_raw_file >> tranformation >> wait_for_processed_file >> end
