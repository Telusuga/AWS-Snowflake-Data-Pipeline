# 🎬 Movie Data Pipeline Project

## 📌 Overview

This project demonstrates a complete end-to-end data pipeline built using AWS and Snowflake. The pipeline extracts movie-related data from an external source (DB/API), processes and transforms the data, and loads it into Snowflake for analytics and dashboarding. It also includes monitoring and alerting mechanisms, with potential enhancements for building a dimensional model using SCD techniques.

![image](https://github.com/user-attachments/assets/a1242d1a-9afc-4c30-9be9-84457214cdc8)



---

🏗️ Architecture

📡 Source Layer
⇨ Movie data pulled from external DB/API.

📦 Ingestion & Staging
✅ Data converted to CSV & Parquet.
✅ Manifest file generated.
✅ Files zipped and uploaded to S3 Landing Zone.

⚙️ Orchestration Layer (Airflow)
✅ Airflow (Dockerized) orchestrates the pipeline:

Triggers extraction and zipping functions on-prem or on EC2.

Monitors S3 for new uploads using sensors.

Triggers Lambda for unzipping when new files land in S3.

Triggers Glue ETL jobs for transformation and validation.

Monitors Glue job completion for downstream dependencies.

Triggers Snowpipe data loads into Snowflake upon successful Glue completion.

Handles failure notifications via SNS if tasks fail.

Schedules periodic runs and backfills as needed.

⚙️ Processing & Transformation
✅ Lambda unzips and validates files on S3 upload.
✅ AWS Glue (Spark) transforms, cleanses, and enriches data.
✅ Writes output as CSV/Parquet into the Processed/Archive S3 bucket.

🏁 Load & Storage
✅ Transformed data stored in S3 (Processed/Archive).
✅ Snowpipe automatically ingests data into Snowflake tables for analytics.

📊 Consumption & Monitoring
✅ Snowflake tables and views power dashboards in Power BI, Tableau, or Looker.
✅ Logs via CloudWatch for Lambda and Glue jobs.
✅ Airflow logs and UI for orchestrated task visibility.
✅ Alerts via SNS (email notifications) on failures.

⚙️ Components Recap
🔄 Data Ingestion Source: External DB/API with movie info.
🗂️ Format: CSV and Parquet with manifest generation.
🗜️ Compression: CSV + manifest zipped.

☁️ AWS S3:

Landing Bucket: Stores zipped data.

Processed Bucket: Receives unzipped files.

Archive Bucket: Stores final transformed data.

🧩 Lambda Function:

Triggered on new file upload.

Unzips and validates files.

Moves content to S3 processed location.

🔥 AWS Glue:

Spark-based transformations.

Cleansing and enrichment.

Writes output to processed/archive bucket.

❄️ Snowflake Integration:

Snowpipe monitors archive bucket.

Auto-loads transformed data into Snowflake tables.

🪐 Airflow Enhancements in the Pipeline:
✅ Modular DAGs for extraction, transformation, and load.
✅ Dynamic task triggering for Lambda, Glue, and Snowpipe orchestration.
✅ XCom for metadata propagation across tasks.
✅ SLA monitoring and failure retries for robust orchestration.
✅ Future integration with Git-based CI/CD for DAG management.

🌟 Future Enhancements
✅ Implement star/snowflake schema in Snowflake.
✅ Enable SCD Type 1/2 using Snowflake Streams and Tasks.
✅ Unit tests & CI/CD pipeline for Lambda, Glue, and Airflow DAGs.
✅ Cost optimization by archiving infrequent data to Glacier.
✅ Enhance metadata tracking using Glue Data Catalog or a custom metadata store.
✅ Integrate with dbt for SQL transformation lineage in Snowflake.


📁 Project Structure

```plaintext
project-root/
├── lambda/
│   ├── Extract.py                    # API/DB data extractor in this file itself we are generating the manifest file
│   ├── Zipping.py                    # Zips files and manifest
│   └── Trigger_job.py                # Triggers Glue job
├── glue_jobs/
│   └── transform_movies.py           # Spark ETL script in AWS Glue
├── Sample_data/
│   ├── Raw_movie_data.csv            # Raw sample data
│   ├── movie_data.parquet            # Parquet version
│   └── manifest.json                 # Metadata manifest
├── diagrams/
│   └── architecture.png              # Visual architecture
├── snowflake/
│   └── Snowflake SQL Commands        # CREATE TABLE + PIPE scripts
├── Airflow/
    └── trigger.py                    # Airflow Code for Triggering
└── README.md                         # Documentation
```
