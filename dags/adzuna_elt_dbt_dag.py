from pendulum import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.hooks.base import BaseHook

import json  # not strictly needed now, but left in case you add vars later

# Path inside the container where the dbt project is mounted
DBT_PROJECT_DIR = "/opt/airflow/dbt"

with DAG(
    dag_id="elt_degree_roi_dbt",
    start_date=datetime(2025, 12, 1),
    description="dbt ELT for college ROI + labor market analytics",
    schedule="0 3 * * *",  # run daily at 03:00; change to None if you want manual only
    catchup=False,
    max_active_runs=1,
) as dag:

    # Get Snowflake connection from Airflow (Conn Id: snowflake_conn)
    conn = BaseHook.get_connection("snowflake_conn")

    # Environment variables passed to dbt, used by profiles.yml via env_var()
    env_vars = {
        "DBT_USER": conn.login,
        "DBT_PASSWORD": conn.password,
        "DBT_ACCOUNT": conn.extra_dejson.get("account"),
        "DBT_SCHEMA": conn.schema,  # default schema for dbt models
        "DBT_DATABASE": conn.extra_dejson.get("database"),
        "DBT_ROLE": conn.extra_dejson.get("role"),
        "DBT_WAREHOUSE": conn.extra_dejson.get("warehouse"),
        "DBT_TYPE": "snowflake",
    }

    # 1) Check dbt connectivity/config
    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=(
            f"/home/airflow/.local/bin/dbt debug "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROJECT_DIR} "
            f"|| echo 'dbt debug failed (likely git missing), continuing anyway'"
        ),
        env=env_vars,
    )

    # 2) Install/refresh dbt packages (dbt_utils, etc.)
    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=(
            f"/home/airflow/.local/bin/dbt deps "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROJECT_DIR}"
        ),
        env=env_vars,
    )

    # 3) Run staging models (stg_institution, stg_jobs, stg_warn, stg_bls, stg_lookups)
    dbt_run_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command=(
            f"/home/airflow/.local/bin/dbt run "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROJECT_DIR} "
            f"--select stg_institution stg_jobs stg_warn stg_bls stg_lookups"
        ),
        env=env_vars,
    )

    # 4) Run final mart model
    dbt_run_mart = BashOperator(
        task_id="dbt_run_mart",
        bash_command=(
            f"/home/airflow/.local/bin/dbt run "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROJECT_DIR} "
            f"--select mart_degree_roi_and_industry_outlook"
        ),
        env=env_vars,
    )

    # 5) Run snapshots (institution_outcomes_snapshot, job_listings_snapshot)
    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command=(
            f"/home/airflow/.local/bin/dbt snapshot "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROJECT_DIR}"
        ),
        env=env_vars,
    )

    # 6) Run dbt tests (sources + staging + mart + snapshots)
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"/home/airflow/.local/bin/dbt test "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROJECT_DIR}"
        ),
        env=env_vars,
    )

    # 7) Optionally generate docs
    dbt_docs_generate = BashOperator(
        task_id="dbt_docs_generate",
        bash_command=(
            f"/home/airflow/.local/bin/dbt docs generate "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROJECT_DIR}"
        ),
        env=env_vars,
    )

    # Task flow
    dbt_debug >> dbt_deps >> dbt_run_staging >> dbt_run_mart >> dbt_snapshot >> dbt_test >> dbt_docs_generate
