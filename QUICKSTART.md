# Quick Start Guide - Adzuna ETL Pipeline

## 🚀 5-Minute Setup

### Step 1: Get API Credentials

1. Go to https://developer.adzuna.com/
2. Sign up for a free account
3. Create an application
4. Note your `App ID` and `App Key`

### Step 2: Install Dependencies

```bash
cd "/Users/dhruv/SJSU/sjsu/data 226/project"
pip install -r requirements.txt
```

### Step 3: Initialize Airflow

```bash
# Set Airflow home
export AIRFLOW_HOME=~/airflow

# Initialize database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### Step 4: Configure Airflow

**Option A: Using Airflow UI (Recommended)**

1. Start Airflow:
   ```bash
   # Terminal 1
   airflow webserver --port 8080
   
   # Terminal 2
   airflow scheduler
   ```

2. Open http://localhost:8080 and login (admin/admin)

3. Set Variables (Admin → Variables → +):
   - `adzuna_app_id`: Your App ID
   - `adzuna_app_key`: Your App Key
   - `adzuna_max_pages`: 200

4. Set Connection (Admin → Connections → +):
   - Connection ID: `snowflake_default`
   - Connection Type: Snowflake
   - Schema: Your database
   - Login: Your username
   - Password: Your password
   - Extra (as JSON):
     ```json
     {
       "account": "your_account.region",
       "warehouse": "your_warehouse",
       "database": "your_database",
       "role": "your_role"
     }
     ```

**Option B: Using Setup Script**

```bash
python setup_airflow.py
# Then update credentials in Airflow UI
```

### Step 5: Deploy DAG and Plugins

```bash
# Copy DAG
cp dags/adzuna_etl_dag.py ~/airflow/dags/

# Copy plugins
cp plugins/*.py ~/airflow/plugins/
```

### Step 6: Create Snowflake Schema

Execute the SQL in your Snowflake console:
```bash
# Open sql/create_job_listings_table.sql
# Copy and run in Snowflake worksheet
```

### Step 7: Run the Pipeline

1. Refresh Airflow UI (http://localhost:8080)
2. Find `adzuna_job_listings_etl` DAG
3. Toggle it ON
4. Click "Trigger DAG" to run manually

## 📊 Verify Success

### Check Airflow Logs
1. Click on the DAG run
2. Check each task (green = success)
3. View logs for details

### Check Snowflake
```sql
-- Count loaded jobs
SELECT COUNT(*) FROM job_listings;

-- View latest jobs
SELECT * FROM vw_latest_job_listings LIMIT 10;

-- Check skill demand
SELECT * FROM vw_skill_demand_index 
ORDER BY job_count DESC 
LIMIT 10;
```

### Check Data Files
```bash
ls -lh data/
# Should see raw_jobs_*.json and transformed_jobs_*.csv
```

## 🔧 Troubleshooting

### DAG not appearing?
```bash
# Check for errors
airflow dags list | grep adzuna

# If not listed, check DAG path
echo $AIRFLOW_HOME
ls ~/airflow/dags/
```

### Import errors?
```bash
# Restart scheduler after copying plugins
pkill -f "airflow scheduler"
airflow scheduler
```

### API errors?
- Verify credentials in Airflow Variables
- Check rate limits (reduce `adzuna_max_pages`)
- Test API: https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=YOUR_ID&app_key=YOUR_KEY

### Snowflake connection errors?
- Test connection in Airflow UI (Test button)
- Verify account identifier format: `account.region`
- Check network/firewall settings

## 📈 Next Steps

1. **Schedule**: DAG runs daily at 2 AM UTC automatically
2. **Monitor**: Check Airflow UI for run history
3. **Analyze**: Query Snowflake views for insights
4. **Scale**: Increase `adzuna_max_pages` for more data

## 📝 Important Notes

- First run may take 30-60 minutes depending on `max_pages`
- Data files stored in `data/` directory
- Logs available in Airflow UI and `~/airflow/logs/`
- API has rate limits - don't set `max_pages` too high

## 🆘 Need Help?

1. Check logs: `~/airflow/logs/dag_id=adzuna_job_listings_etl/`
2. Run tests: `python test_pipeline.py`
3. Check README.md for detailed documentation
4. Review Airflow docs: https://airflow.apache.org/docs/

---

**You're all set!** 🎉 The pipeline will now run daily and populate your Snowflake database with job market data.
