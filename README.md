# 🎬 Movie Data Pipeline Project

## 📌 Overview

This project demonstrates a complete end-to-end data pipeline built using AWS and Snowflake. The pipeline extracts movie-related data from an external source (DB/API), processes and transforms the data, and loads it into Snowflake for analytics and dashboarding. It also includes monitoring and alerting mechanisms, with potential enhancements for building a dimensional model using SCD techniques.

---

## 🏗️ Architecture

[1] External Source (DB/API)
    └── Pull movie data
    └── Convert to CSV and Parquet
    └── Generate manifest.json for metadata

[2] Zip & Upload
    └── Bundle CSV + Parquet + Manifest
    └── Upload ZIP to AWS S3 (Landing Bucket)

[3] Lambda Function
    └── Triggered by ZIP upload
    └── Unzips and validates files
    └── Places into S3 (Processed Bucket)

[4] AWS Glue Job (Spark)
    └── Triggered by new files
    └── Performs transformations
    └── Validates schema and data
    └── Writes transformed CSV to Archive Bucket

[5] Snowflake Ingestion
    └── Snowpipe monitors Archive Bucket
    └── Loads CSV into Snowflake tables

[6] Consumption Layer
    └── Dashboards via Power BI / Tableau
    └── Monitoring via CloudWatch
    └── Alerting via SNS (Email on Failure)




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
