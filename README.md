# 🎬 Movie Data Pipeline Project

## 📌 Overview

This project demonstrates a complete end-to-end data pipeline built using AWS and Snowflake. The pipeline extracts movie-related data from an external source (DB/API), processes and transforms the data, and loads it into Snowflake for analytics and dashboarding. It also includes monitoring and alerting mechanisms, with potential enhancements for building a dimensional model using SCD techniques.

---

## 🏗️ Architecture

📡 Source Layer
    ⇨ Movie data pulled from external DB/API

📦 Ingestion & Staging
    ⇨ Data converted to CSV & Parquet
    ⇨ Manifest file generated
    ⇨ Files zipped and uploaded to S3 (Landing Zone)

⚙️ Processing & Transformation
    ⇨ Lambda unzips and validates files
    ⇨ AWS Glue (Spark) transforms and validates data

🏁 Load & Storage
    ⇨ Transformed data stored in S3 (Archive)
    ⇨ Snowpipe ingests data into Snowflake

📊 Consumption & Monitoring
    ⇨ Dashboards via Power BI / Tableau
    ⇨ Logs via CloudWatch
    ⇨ Alerts via SNS (Email notifications)





⚙️ Components
🔄 Data Ingestion
Source: External DB/API with movie info

Format: Converted to CSV and Parquet

Metadata: Manifest file created

Compression: CSV + Manifest zipped

☁️ AWS S3
Landing Bucket: Stores zipped data

Processed Bucket: Receives unzipped files via Lambda

Archive Bucket: Stores final transformed CSVs

🧩 Lambda Function
Triggered on file upload

Unzips incoming archive

Moves contents to correct S3 location

🔥 AWS Glue Job
Spark-based transformation of CSV/Parquet

Data cleansing and enrichment

Writes output as CSV into the archive bucket

❄️ Snowflake Integration
Snowpipe monitors archive bucket

Automatically loads transformed data into target tables

📊 Consumption Layer
Snowflake tables form the base for dashboards

Compatible with Power BI, Tableau, and other BI tools

🚨 Monitoring & Alerting
CloudWatch for logging Glue/Lambda

AWS SNS for failure notifications to registered email addresses

🌟 Future Enhancements
Implement star/snowflake schema in Snowflake

Enable SCD Type 1 / Type 2 using Snowflake Streams and Tasks

Add unit tests & CI/CD pipeline for Lambda and Glue jobs

Cost optimization by moving infrequent data to Glacier

Enhance metadata tracking using AWS Glue Data Catalog or custom metadata store



📁 Project Structure

├── lambda/
│   └── unzip_handler.py               # AWS Lambda function to unzip & validate files
├── glue_jobs/
│   └── transform_movies.py           # AWS Glue Spark script for transformation & validation
├── data_samples/
│   ├── movies.csv                    # Sample movie dataset (raw)
│   ├── movies.parquet                # Parquet version for Glue processing
│   └── manifest.json                 # Metadata file describing batch contents
├── utils/
│   └── generate_manifest.py          # Utility to auto-generate manifest files
├── diagrams/
│   └── architecture.png              # Visual architecture of the pipeline
├── scripts/
│   ├── Extract.py                    # Script to pull data from external API/DB
│   ├── Zipping.py                    # Script to zip data + manifest
│   ├── Trigger_job.py                # Optional trigger for Glue jobs
├── snowflake/
│   └── Snowflake SQL Commands        # Snowflake table creation and Snowpipe scripts
├── AWS Glue Spark Job                # Job script (can be moved to glue_jobs/)
├── README.md                         # Documentation
