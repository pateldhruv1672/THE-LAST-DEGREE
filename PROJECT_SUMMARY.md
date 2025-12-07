# Adzuna ETL Pipeline - Project Summary

## 📁 Complete File Structure

```
/Users/dhruv/SJSU/sjsu/data 226/project/
│
├── dags/
│   └── adzuna_etl_dag.py              # Main Airflow DAG definition
│
├── plugins/
│   ├── adzuna_extraction.py           # Extract from Adzuna API
│   ├── adzuna_transformation.py       # Transform job data
│   └── adzuna_loading.py              # Load to Snowflake
│
├── sql/
│   └── create_job_listings_table.sql  # Snowflake schema & views
│
├── data/                              # Temporary storage for pipeline runs
│   └── .gitkeep                       # Keep directory in git
│
├── requirements.txt                   # Python dependencies
├── README.md                          # Comprehensive documentation
├── QUICKSTART.md                      # Fast setup guide
├── ARCHITECTURE.md                    # Technical architecture
├── setup_airflow.py                   # Automated setup script
├── test_pipeline.py                   # Component testing
├── .env.example                       # Environment template
└── .gitignore                         # Git ignore rules
```

## 🎯 Key Features

### ✅ Complete ETL Pipeline
- **Extract**: Pagination-aware API client with retry logic
- **Transform**: HTML cleaning, date parsing, salary normalization
- **Load**: Staging table + UPSERT pattern for Snowflake

### ✅ Airflow Integration
- Individual tasks for each ETL step
- Snowflake operators for schema management
- XCom for inter-task communication
- Email alerts on failure

### ✅ Secure Credential Management
- API keys stored in Airflow Variables
- Database credentials in Airflow Connections
- No secrets in code or version control

### ✅ Data Quality
- Input validation at extraction
- Transformation quality checks
- Post-load verification queries
- Deduplication logic

### ✅ Analytics-Ready Schema
- Optimized indexes for query performance
- Pre-built views for common analytics
- Partitioning by load_date
- Support for time-series analysis

## 📊 Data Pipeline Specifications

| Aspect | Specification |
|--------|--------------|
| **Source** | Adzuna Job Search API |
| **Volume** | ~10,000 jobs per run (configurable up to 1M+) |
| **Frequency** | Daily at 2 AM UTC |
| **Latency** | 30-60 minutes per run |
| **Storage** | Snowflake data warehouse |
| **Orchestrator** | Apache Airflow |
| **Retry Policy** | 3 attempts with 5-minute delays |

## 🔧 Configuration Points

### Airflow Variables
```
adzuna_app_id      → Your Adzuna App ID
adzuna_app_key     → Your Adzuna App Key
adzuna_max_pages   → Number of pages to fetch (default: 200)
```

### Airflow Connections
```
snowflake_default  → Snowflake connection details
```

### DAG Parameters
```python
schedule_interval  → '0 2 * * *' (Daily at 2 AM UTC)
max_active_runs    → 1 (Prevent overlapping runs)
retries            → 3 (Retry failed tasks 3 times)
retry_delay        → 5 minutes
execution_timeout  → 2 hours
```

## 📈 Use Cases Enabled

1. **Skill Demand Index**
   - Track job postings by category over time
   - Identify trending skills and technologies
   - Forecast future skill requirements

2. **Salary Trend Analysis**
   - Monitor salary ranges by role and location
   - Calculate ROI for education/training
   - Benchmark compensation data

3. **Job Market Intelligence**
   - Geographic distribution of opportunities
   - Company hiring patterns
   - Industry growth indicators

4. **Career Planning**
   - Identify high-demand roles
   - Compare locations for job seekers
   - Track career path transitions

## 🚀 Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] Apache Airflow 2.8+ installed
- [ ] Snowflake account created
- [ ] Adzuna API credentials obtained
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Airflow database initialized (`airflow db init`)
- [ ] Airflow user created
- [ ] Airflow Variables configured
- [ ] Snowflake Connection configured
- [ ] Snowflake schema created
- [ ] DAG and plugins copied to Airflow directories
- [ ] Airflow webserver and scheduler running
- [ ] DAG enabled in Airflow UI
- [ ] Test run executed successfully

## 📚 Documentation Guide

| Document | Purpose | Audience |
|----------|---------|----------|
| **README.md** | Complete project documentation | All users |
| **QUICKSTART.md** | Fast 5-minute setup | New users |
| **ARCHITECTURE.md** | Technical deep-dive with diagrams | Developers/Engineers |
| **This file** | Project overview and summary | Stakeholders/Management |

## 🧪 Testing

### Unit Tests
```bash
python test_pipeline.py
```

### Manual DAG Test
```bash
# Test DAG syntax
airflow dags test adzuna_job_listings_etl 2025-12-06

# Test individual task
airflow tasks test adzuna_job_listings_etl extract_adzuna_jobs 2025-12-06
```

### Integration Test
1. Trigger DAG in Airflow UI
2. Monitor task execution
3. Verify data in Snowflake
4. Check data quality metrics

## 🔍 Monitoring & Observability

### Airflow UI Metrics
- DAG run success rate
- Task execution times
- XCom values (job counts)
- Log files for debugging

### Snowflake Metrics
- Row counts per load_date
- Data quality statistics
- Query performance
- Storage usage

### Key Performance Indicators
- Pipeline success rate: > 95%
- Average execution time: < 60 minutes
- Data quality: > 99% valid records
- API error rate: < 1%

## 🛠️ Maintenance Tasks

### Daily
- Monitor DAG runs in Airflow UI
- Check for failed tasks
- Review error logs if failures occur

### Weekly
- Review data quality metrics
- Analyze execution time trends
- Check Snowflake storage usage

### Monthly
- Rotate API keys (security best practice)
- Review and optimize Snowflake queries
- Update documentation if needed
- Archive old data files

### Quarterly
- Dependency updates (`pip list --outdated`)
- Performance optimization
- Schema evolution planning

## 🤝 Team Responsibilities

### Data Engineers
- Maintain pipeline code
- Optimize performance
- Handle failures and incidents
- Update dependencies

### Data Analysts
- Query Snowflake views
- Build analytics dashboards
- Provide feedback on data quality
- Request new features

### DevOps
- Manage Airflow infrastructure
- Monitor system resources
- Handle backups and disaster recovery
- Manage credentials and secrets

## 📞 Support

### Common Issues
1. **DAG not appearing**: Check DAG file path and syntax
2. **API rate limits**: Reduce `adzuna_max_pages` variable
3. **Snowflake connection**: Verify credentials and network
4. **Out of memory**: Reduce batch sizes in loading script

### Getting Help
1. Check Airflow task logs first
2. Review documentation (README, QUICKSTART)
3. Run test script: `python test_pipeline.py`
4. Check GitHub issues (if applicable)

## 🎓 Learning Resources

- [Adzuna API Docs](https://developer.adzuna.com/docs/search)
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Snowflake Docs](https://docs.snowflake.com/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

## 📊 Success Criteria

✅ **Pipeline is successful when:**
- Runs daily without manual intervention
- Loads 10,000+ job records per run
- Completes within 60-minute SLA
- Maintains > 99% data quality
- Enables real-time ROI forecasting
- Supports Skill Demand Index calculation

---

**Project Status**: ✅ Complete and Production-Ready

**Created**: December 6, 2025  
**Version**: 1.0.0  
**Last Updated**: December 6, 2025  
**Maintainer**: SJSU Data Engineering Team
