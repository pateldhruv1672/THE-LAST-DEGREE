# Adzuna Job Listings ETL Pipeline

An Apache Airflow-based ETL pipeline that extracts job listing data from the Adzuna API, transforms it, and loads it into Snowflake for analytics and forecasting.

## 📋 Overview

- **Data Source**: Adzuna API (https://developer.adzuna.com/)
- **Volume**: ~1 million active US job listings
- **Update Frequency**: Daily at 2 AM UTC
- **Purpose**: Feed Skill Demand Index and salary trends for ROI forecasts

## 🏗️ Architecture

```
Adzuna API → Extract (JSON) → Transform (CSV) → Load (Snowflake)
                 ↓                 ↓                  ↓
            Raw Data         Cleaned Data      Analytics Tables
```

### Pipeline Components

1. **Extraction** (`plugins/adzuna_extraction.py`)
   - Fetches job listings from Adzuna API
   - Handles pagination and rate limiting
   - Extracts: job_title, company, salary_min/max, description, posting_date, location, category

2. **Transformation** (`plugins/adzuna_transformation.py`)
   - Cleans HTML from descriptions
   - Normalizes salary data
   - Parses and validates dates
   - Removes duplicates

3. **Loading** (`plugins/adzuna_loading.py`)
   - Loads data into Snowflake using staging tables
   - Performs upsert (merge) operations
   - Generates load statistics

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Apache Airflow 2.8+
- Snowflake account
- Adzuna API credentials (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   cd /Users/dhruv/SJSU/sjsu/data\ 226/project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Airflow** (if not already done)
   ```bash
   export AIRFLOW_HOME=~/airflow
   airflow db init
   airflow users create \
       --username admin \
       --firstname Admin \
       --lastname User \
       --role Admin \
       --email admin@example.com
   ```

4. **Set up Airflow Variables**
   
   Navigate to Airflow UI → Admin → Variables and create:
   
   | Key | Value | Description |
   |-----|-------|-------------|
   | `adzuna_app_id` | Your App ID | From Adzuna developer portal |
   | `adzuna_app_key` | Your App Key | From Adzuna developer portal |
   | `adzuna_max_pages` | 200 | Number of pages to fetch (50 jobs/page) |

5. **Set up Airflow Connection for Snowflake**
   
   Navigate to Airflow UI → Admin → Connections and create:
   
   - **Connection ID**: `snowflake_default`
   - **Connection Type**: Snowflake
   - **Schema**: Your database name
   - **Login**: Your Snowflake username
   - **Password**: Your Snowflake password
   - **Account**: Your Snowflake account identifier
   - **Warehouse**: Your Snowflake warehouse
   - **Database**: Your Snowflake database
   - **Role**: Your Snowflake role (optional)

6. **Create Snowflake Schema**
   
   Execute the SQL script in your Snowflake console:
   ```bash
   # Copy contents of sql/create_job_listings_table.sql
   # and execute in Snowflake
   ```

7. **Copy DAG to Airflow**
   ```bash
   # If using default Airflow home
   cp -r dags/* ~/airflow/dags/
   cp -r plugins/* ~/airflow/plugins/
   ```

8. **Start Airflow**
   ```bash
   # Terminal 1: Webserver
   airflow webserver --port 8080
   
   # Terminal 2: Scheduler
   airflow scheduler
   ```

9. **Enable the DAG**
   - Open Airflow UI at http://localhost:8080
   - Find `adzuna_job_listings_etl` DAG
   - Toggle it ON

## 📊 Data Schema

### Snowflake Table: `job_listings`

| Column | Type | Description |
|--------|------|-------------|
| job_id | VARCHAR(255) | Unique job identifier (PK) |
| load_date | DATE | ETL execution date (PK) |
| job_title | VARCHAR(500) | Job title |
| company | VARCHAR(500) | Company name |
| salary_min | FLOAT | Minimum salary |
| salary_max | FLOAT | Maximum salary |
| salary_avg | FLOAT | Average salary (calculated) |
| description | TEXT | Job description (HTML cleaned) |
| posting_date | DATE | When job was posted |
| location | VARCHAR(500) | Full location string |
| city | VARCHAR(255) | Parsed city |
| state | VARCHAR(100) | Parsed state |
| category | VARCHAR(255) | Job category/skill area |
| contract_type | VARCHAR(100) | Contract type |
| contract_time | VARCHAR(100) | Full-time/Part-time |
| latitude | FLOAT | Geolocation |
| longitude | FLOAT | Geolocation |
| redirect_url | TEXT | Application URL |
| extracted_at | TIMESTAMP | Extraction timestamp |

## 📈 Analytics Views

The pipeline creates several analytical views:

- **vw_latest_job_listings**: Most recent job listings
- **vw_skill_demand_index**: Job demand by category
- **vw_salary_trends**: Salary trends over time
- **vw_job_market_by_location**: Geographic job distribution
- **vw_company_hiring_trends**: Company hiring patterns

## 🔧 Configuration

### Adjusting Data Volume

Modify the `adzuna_max_pages` variable in Airflow:
- 100 pages = ~5,000 jobs
- 200 pages = ~10,000 jobs
- For full coverage (~1M jobs), set to 20,000 pages

⚠️ **Note**: Higher page counts will increase execution time and API usage.

### Schedule Modification

Edit `dags/adzuna_etl_dag.py`:
```python
schedule_interval='0 2 * * *',  # Daily at 2 AM UTC
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors in Airflow**
   - Ensure plugins are in `$AIRFLOW_HOME/plugins/`
   - Restart Airflow scheduler

2. **API Rate Limiting**
   - Reduce `adzuna_max_pages`
   - Add delays between requests (modify extraction script)

3. **Snowflake Connection Errors**
   - Verify connection details in Airflow UI
   - Test connection using `Test` button
   - Check firewall/network settings

4. **Out of Memory Errors**
   - Reduce batch size in loading script
   - Process data in smaller chunks

## 📁 Project Structure

```
project/
├── dags/
│   └── adzuna_etl_dag.py          # Main Airflow DAG
├── plugins/
│   ├── adzuna_extraction.py       # API extraction logic
│   ├── adzuna_transformation.py   # Data transformation
│   └── adzuna_loading.py          # Snowflake loading
├── sql/
│   └── create_job_listings_table.sql  # Snowflake schema
├── data/                          # Temporary data storage
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. **Use Airflow Variables** for all secrets
3. **Enable encryption** for Snowflake connections
4. **Rotate API keys** periodically
5. **Limit Snowflake role permissions** to minimum required

## 📝 Monitoring

The DAG includes:
- Email alerts on failure
- XCom metrics for job counts
- Data quality checks after loading
- Execution time tracking

Monitor in Airflow UI:
- Graph View: Task dependencies
- Tree View: Historical runs
- Logs: Detailed execution logs

## 🤝 Contributing

1. Create feature branch
2. Test locally with small data samples
3. Validate SQL queries in Snowflake
4. Submit pull request with description

## 📄 License

This project is for educational purposes as part of SJSU Data Engineering coursework.

## 🔗 Resources

- [Adzuna API Documentation](https://developer.adzuna.com/docs)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Snowflake Documentation](https://docs.snowflake.com/)
- [Airflow-Snowflake Provider](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/)

## 📧 Support

For issues or questions, contact the data engineering team or create an issue in the repository.

---

**Last Updated**: December 6, 2025
**Version**: 1.0.0
**Author**: Data Engineering Team
