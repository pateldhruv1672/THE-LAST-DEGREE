# Adzuna ETL Pipeline Architecture

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ADZUNA ETL PIPELINE                         │
│                     (Apache Airflow Orchestration)                  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────┐
│  ADZUNA API │
│  (Source)   │
│             │
│ • 1M+ Jobs  │
│ • Daily     │
│ • REST API  │
└──────┬──────┘
       │
       │ HTTP GET Requests
       │ (Paginated: 50/page)
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     TASK 1: CREATE SCHEMA                           │
│                  SnowflakeOperator                                  │
│  • Creates job_listings table                                      │
│  • Creates indexes for performance                                 │
│  • Creates analytical views                                        │
└─────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     TASK 2: EXTRACT                                 │
│                  PythonOperator                                     │
│  Script: plugins/adzuna_extraction.py                              │
│                                                                     │
│  Input:                                                             │
│  • Airflow Variables: adzuna_app_id, adzuna_app_key                │
│  • Configuration: max_pages (default: 200)                         │
│                                                                     │
│  Process:                                                           │
│  • Paginate through API results                                    │
│  • Extract job fields                                              │
│  • Handle rate limiting                                            │
│  • Error handling & retries                                        │
│                                                                     │
│  Output:                                                            │
│  • File: data/raw_jobs_{{ ds }}.json                              │
│  • Format: JSON with metadata                                      │
│  • Size: ~10-50 MB per run                                         │
└─────────────────────────────────────────────────────────────────────┘
       │
       │ raw_jobs_{{ ds }}.json
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    TASK 3: TRANSFORM                                │
│                  PythonOperator                                     │
│  Script: plugins/adzuna_transformation.py                          │
│                                                                     │
│  Input:                                                             │
│  • File: data/raw_jobs_{{ ds }}.json                              │
│                                                                     │
│  Transformations:                                                   │
│  • Clean HTML from descriptions                                    │
│  • Parse dates (ISO → YYYY-MM-DD)                                  │
│  • Normalize salaries (min/max/avg)                                │
│  • Parse location → city, state                                    │
│  • Remove duplicates by job_id                                     │
│  • Data validation & quality checks                                │
│                                                                     │
│  Output:                                                            │
│  • File: data/transformed_jobs_{{ ds }}.csv                       │
│  • Format: Clean CSV ready for loading                            │
└─────────────────────────────────────────────────────────────────────┘
       │
       │ transformed_jobs_{{ ds }}.csv
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      TASK 4: LOAD                                   │
│                  PythonOperator                                     │
│  Script: plugins/adzuna_loading.py                                 │
│                                                                     │
│  Input:                                                             │
│  • File: data/transformed_jobs_{{ ds }}.csv                       │
│  • Connection: snowflake_default                                   │
│                                                                     │
│  Process:                                                           │
│  1. Create staging table (temporary)                               │
│  2. Bulk load CSV → staging table                                  │
│  3. MERGE staging → target table (UPSERT)                          │
│  4. Generate load statistics                                       │
│                                                                     │
│  Output:                                                            │
│  • Target Table: job_listings                                      │
│  • Operation: INSERT new / UPDATE existing                         │
└─────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  TASK 5: QUALITY CHECKS                             │
│                  SnowflakeOperator                                  │
│                                                                     │
│  Validations:                                                       │
│  • Count total records loaded                                      │
│  • Verify unique job_ids                                           │
│  • Check date ranges                                               │
│  • Validate salary data                                            │
│  • Log statistics to Airflow                                       │
└─────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       SNOWFLAKE DATABASE                            │
│                                                                     │
│  Tables:                                                            │
│  └─ job_listings (main table)                                      │
│                                                                     │
│  Views:                                                             │
│  ├─ vw_latest_job_listings                                         │
│  ├─ vw_skill_demand_index                                          │
│  ├─ vw_salary_trends                                               │
│  ├─ vw_job_market_by_location                                      │
│  └─ vw_company_hiring_trends                                       │
│                                                                     │
│  Indexes:                                                           │
│  ├─ idx_job_category (category, load_date)                         │
│  ├─ idx_job_location (state, city, load_date)                      │
│  ├─ idx_job_salary (posting_date, salary_avg)                      │
│  ├─ idx_job_company (company, load_date)                           │
│  └─ idx_job_posting_date (posting_date DESC)                       │
└─────────────────────────────────────────────────────────────────────┘
       │
       │ SQL Queries
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        ANALYTICS & BI                               │
│                                                                     │
│  Use Cases:                                                         │
│  • Skill Demand Index calculation                                  │
│  • Salary trend analysis for ROI forecasts                         │
│  • Job market geographic distribution                              │
│  • Company hiring patterns                                         │
│  • Career path recommendations                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔄 Task Dependencies

```
create_table_task
       ↓
extract_task
       ↓
transform_task
       ↓
load_task
       ↓
quality_check_task
```

## 📦 Component Breakdown

### 1. Extraction (adzuna_extraction.py)
- **Class**: `AdzunaAPIClient`
- **Key Methods**:
  - `fetch_jobs_page()`: Get single page of results
  - `extract_job_fields()`: Parse API response
  - `fetch_all_jobs()`: Paginate through all results
- **Credentials**: Stored in Airflow Variables
- **Output**: JSON file with job listings + metadata

### 2. Transformation (adzuna_transformation.py)
- **Class**: `JobDataTransformer`
- **Key Methods**:
  - `clean_html()`: Remove HTML tags
  - `parse_date()`: Standardize dates
  - `normalize_salary()`: Clean salary data
  - `clean_location()`: Parse city/state
  - `validate_job()`: Data quality checks
- **Input**: Raw JSON
- **Output**: Clean CSV

### 3. Loading (adzuna_loading.py)
- **Class**: `SnowflakeLoader`
- **Key Methods**:
  - `create_staging_table()`: Temp table for batch load
  - `load_csv_to_staging()`: Bulk insert
  - `merge_staging_to_target()`: UPSERT operation
  - `get_load_statistics()`: Data quality metrics
- **Connection**: Airflow Snowflake connection
- **Strategy**: Staging → Merge (prevents duplicates)

## 🕐 Execution Schedule

```
Schedule: 0 2 * * * (Daily at 2:00 AM UTC)

Timeline:
02:00 - Start execution
02:01 - Create/verify schema
02:02 - Begin extraction (30-45 min)
02:45 - Transformation (5-10 min)
02:55 - Load to Snowflake (10-15 min)
03:10 - Quality checks
03:15 - Complete
```

## 💾 Data Volume Estimates

| Pages | Jobs/Run | JSON Size | CSV Size | Load Time |
|-------|----------|-----------|----------|-----------|
| 50    | ~2,500   | ~3 MB     | ~1 MB    | ~5 min    |
| 100   | ~5,000   | ~6 MB     | ~2 MB    | ~10 min   |
| 200   | ~10,000  | ~12 MB    | ~4 MB    | ~20 min   |
| 500   | ~25,000  | ~30 MB    | ~10 MB   | ~45 min   |
| 1000  | ~50,000  | ~60 MB    | ~20 MB   | ~90 min   |

## 🔐 Security Architecture

```
Credentials Management:

Adzuna API:
├─ App ID → Airflow Variable (encrypted)
└─ App Key → Airflow Variable (encrypted)

Snowflake:
├─ Username → Airflow Connection (encrypted)
├─ Password → Airflow Connection (encrypted)
├─ Account → Airflow Connection
└─ Warehouse → Airflow Connection

Never stored in:
├─ Code files ❌
├─ Git repository ❌
└─ Plain text ❌
```

## 📊 Data Schema

```
job_listings (Table)
├─ job_id VARCHAR(255) [PK]
├─ load_date DATE [PK]
├─ job_title VARCHAR(500)
├─ company VARCHAR(500)
├─ salary_min FLOAT
├─ salary_max FLOAT
├─ salary_avg FLOAT
├─ description TEXT
├─ posting_date DATE
├─ location VARCHAR(500)
├─ city VARCHAR(255)
├─ state VARCHAR(100)
├─ category VARCHAR(255)
├─ contract_type VARCHAR(100)
├─ contract_time VARCHAR(100)
├─ latitude FLOAT
├─ longitude FLOAT
├─ redirect_url TEXT
└─ extracted_at TIMESTAMP
```

## 🎯 Success Metrics

**Per Run:**
- Jobs Extracted: 10,000+ (with 200 pages)
- Jobs Transformed: 95%+ of extracted
- Jobs Loaded: 100% of transformed
- Load Time: < 60 minutes
- Data Quality: > 99% valid records

**Daily Metrics:**
- Success Rate: > 95%
- API Errors: < 1%
- Duplicate Rate: < 0.1%
- Schema Violations: 0

---

Last Updated: December 6, 2025
