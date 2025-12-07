# 📚 Adzuna ETL Pipeline - Documentation Index

Welcome to the Adzuna Job Listings ETL Pipeline! This index will help you find the right documentation for your needs.

## 🎯 Quick Navigation

### For New Users
👉 **Start here**: [QUICKSTART.md](QUICKSTART.md)
- 5-minute setup guide
- Step-by-step installation
- First pipeline run

### For Detailed Setup
📖 **Read**: [README.md](README.md)
- Complete project documentation
- Comprehensive setup instructions
- Configuration options
- Troubleshooting guide

### For Technical Understanding
🏗️ **Review**: [ARCHITECTURE.md](ARCHITECTURE.md)
- Data flow diagrams
- Component breakdown
- Technical specifications
- Performance metrics

### For Project Overview
📊 **See**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- High-level overview
- Key features
- Success criteria
- Team responsibilities

## 📁 File Reference

### Core Pipeline Files

| File | Purpose | Location |
|------|---------|----------|
| `adzuna_etl_dag.py` | Main Airflow DAG | `dags/` |
| `adzuna_extraction.py` | Extract from API | `plugins/` |
| `adzuna_transformation.py` | Transform data | `plugins/` |
| `adzuna_loading.py` | Load to Snowflake | `plugins/` |
| `create_job_listings_table.sql` | Snowflake schema | `sql/` |

### Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |
| `.gitignore` | Git ignore rules |

### Helper Scripts

| File | Purpose |
|------|---------|
| `setup_airflow.py` | Automated Airflow setup |
| `test_pipeline.py` | Component testing |
| `verify_setup.sh` | Setup verification |

### Documentation Files

| File | Best For |
|------|----------|
| `QUICKSTART.md` | Getting started quickly |
| `README.md` | Complete reference |
| `ARCHITECTURE.md` | Understanding design |
| `PROJECT_SUMMARY.md` | Overview & status |
| `INDEX.md` | Finding documentation (this file) |

## 🚀 Getting Started Workflow

```
1. Read QUICKSTART.md
   ↓
2. Install dependencies (requirements.txt)
   ↓
3. Run verify_setup.sh
   ↓
4. Configure Airflow (variables & connections)
   ↓
5. Deploy DAG and plugins
   ↓
6. Test with test_pipeline.py
   ↓
7. Enable DAG in Airflow UI
   ↓
8. Monitor first run
   ↓
9. Verify data in Snowflake
   ↓
10. Review ARCHITECTURE.md for optimization
```

## 📞 Where to Find Answers

### "How do I get started?"
→ [QUICKSTART.md](QUICKSTART.md)

### "How do I configure the pipeline?"
→ [README.md](README.md) - Configuration section

### "How does the pipeline work?"
→ [ARCHITECTURE.md](ARCHITECTURE.md)

### "What credentials do I need?"
→ [QUICKSTART.md](QUICKSTART.md) - Step 1 & Step 4

### "How do I troubleshoot errors?"
→ [README.md](README.md) - Troubleshooting section

### "What SQL queries can I run?"
→ [sql/create_job_listings_table.sql](sql/create_job_listings_table.sql) - Sample queries section

### "How do I test the pipeline?"
→ Run `python test_pipeline.py` or see [README.md](README.md) - Testing section

### "What data is available?"
→ [ARCHITECTURE.md](ARCHITECTURE.md) - Data Schema section

### "How do I monitor the pipeline?"
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Monitoring section

### "What's the project status?"
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Success Criteria section

## 🎓 Learning Path

### Day 1: Setup & First Run
1. Read QUICKSTART.md (15 min)
2. Install and configure (30 min)
3. Run first pipeline (60 min)
4. Verify data in Snowflake (15 min)

### Day 2: Deep Dive
1. Read README.md (30 min)
2. Study ARCHITECTURE.md (30 min)
3. Review code in plugins/ (60 min)
4. Experiment with configurations (30 min)

### Day 3: Optimization & Analytics
1. Review Snowflake views (30 min)
2. Write custom analytics queries (60 min)
3. Optimize pipeline parameters (30 min)
4. Set up monitoring (30 min)

## 🔧 Common Tasks

### Task: Install Dependencies
```bash
pip install -r requirements.txt
```
**See**: requirements.txt

### Task: Initialize Airflow
```bash
airflow db init
```
**See**: [QUICKSTART.md](QUICKSTART.md) - Step 3

### Task: Configure Credentials
**See**: [QUICKSTART.md](QUICKSTART.md) - Step 4

### Task: Deploy to Airflow
```bash
cp dags/*.py ~/airflow/dags/
cp plugins/*.py ~/airflow/plugins/
```
**See**: [QUICKSTART.md](QUICKSTART.md) - Step 5

### Task: Create Snowflake Tables
**See**: [sql/create_job_listings_table.sql](sql/create_job_listings_table.sql)

### Task: Test Pipeline
```bash
python test_pipeline.py
```
**See**: test_pipeline.py

### Task: Verify Setup
```bash
./verify_setup.sh
```
**See**: verify_setup.sh

### Task: Monitor Pipeline
**See**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Monitoring section

## 📊 Data & Analytics

### Available Data Fields
- Job ID, Title, Company
- Salary (min, max, avg)
- Location (full, city, state, coordinates)
- Category, Contract Type
- Posting Date, Description
- **See**: [ARCHITECTURE.md](ARCHITECTURE.md) - Data Schema

### Pre-built Views
- Latest job listings
- Skill demand index
- Salary trends
- Job market by location
- Company hiring trends
- **See**: [sql/create_job_listings_table.sql](sql/create_job_listings_table.sql)

### Sample Analytics Queries
**See**: [sql/create_job_listings_table.sql](sql/create_job_listings_table.sql) - Sample Queries section

## 🐛 Troubleshooting

| Issue | Where to Look |
|-------|--------------|
| DAG not appearing | [README.md](README.md) - Troubleshooting |
| API errors | [README.md](README.md) - Troubleshooting |
| Snowflake connection | [README.md](README.md) - Troubleshooting |
| Import errors | [README.md](README.md) - Troubleshooting |
| Setup verification | Run `./verify_setup.sh` |

## 🤝 Contributing

### Before Making Changes
1. Understand architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
2. Test changes: `python test_pipeline.py`
3. Update documentation if needed
4. Follow coding standards in existing files

### Adding Features
1. Update appropriate plugin file
2. Modify DAG if needed
3. Update SQL schema if needed
4. Document in README.md
5. Add tests to test_pipeline.py

## 📈 Performance & Optimization

### Pipeline Performance
**See**: [ARCHITECTURE.md](ARCHITECTURE.md) - Data Volume Estimates

### Query Optimization
**See**: [sql/create_job_listings_table.sql](sql/create_job_listings_table.sql) - Indexes section

### Configuration Tuning
**See**: [README.md](README.md) - Configuration section

## 🎯 Use Cases

### Skill Demand Analysis
**See**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Use Cases

### Salary Trend Forecasting
**See**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Use Cases

### Job Market Intelligence
**See**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Use Cases

## 📞 Support & Resources

### Internal Documentation
- All `.md` files in this directory

### External Resources
- [Adzuna API Docs](https://developer.adzuna.com/)
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Snowflake Docs](https://docs.snowflake.com/)

### Getting Help
1. Check relevant documentation above
2. Review logs in Airflow UI
3. Run `python test_pipeline.py`
4. Run `./verify_setup.sh`

## 📝 Quick Reference Card

```
# Install
pip install -r requirements.txt

# Initialize
airflow db init

# Test
python test_pipeline.py

# Verify
./verify_setup.sh

# Deploy
cp dags/*.py ~/airflow/dags/
cp plugins/*.py ~/airflow/plugins/

# Run
airflow webserver --port 8080  # Terminal 1
airflow scheduler              # Terminal 2

# Access
http://localhost:8080
```

---

**Last Updated**: December 6, 2025  
**Version**: 1.0.0  
**Project**: SJSU Data 226 - Adzuna ETL Pipeline

**Need help?** Start with [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md)
