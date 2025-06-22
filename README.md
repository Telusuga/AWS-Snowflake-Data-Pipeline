# AWS-Snowflake-Data-Pipeline
This repo consists of the aws snowflake pipeline using glue for transformation


# 🎬 Movie Data Pipeline Project

## 📌 Overview

This project demonstrates a complete end-to-end data pipeline built using AWS and Snowflake. The pipeline extracts movie-related data from an external source (DB/API), processes and transforms the data, and loads it into Snowflake for analytics and dashboarding. It also includes monitoring and alerting mechanisms, with potential enhancements for building a dimensional model using SCD techniques.

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A[External Source (DB/API)] --> B[CSV + Parquet + Manifest]
    B --> C[Zip Files]
    C --> D[S3 Landing Bucket]
    D --> E[Lambda (Unzip + Validate)]
    E --> F[S3 Processed Bucket]
    F --> G[AWS Glue (Transform + Validate)]
    G --> H[S3 Archive Bucket]
    H --> I[Snowpipe]
    I --> J[Snowflake Table]
    J --> K[Power BI / Tableau]
    J --> L[SNS Alerts on Failure]
```



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
