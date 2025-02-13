import os

# Note: DagBag.process_file skips files without "airflow" or "DAG" in them

from data_science_pipeline.utils.dags import (
    create_dag,
    create_run_notebook_operator
)


DEFAULT_PEERSCOUT_RECOMMEND_SCHEDULE = '@hourly'

DATA_SCIENCE_PEERSCOUT_RECOMMEND_SCHEDULE_INTERVAL_ENV_NAME = (
    "DATA_SCIENCE_PEERSCOUT_RECOMMEND_SCHEDULE_INTERVAL"
)


DAG_ID = "Data_Science_PeerScout_Recommend_Reviewing_Editors"


def get_schedule_interval() -> str:
    return os.getenv(
        DATA_SCIENCE_PEERSCOUT_RECOMMEND_SCHEDULE_INTERVAL_ENV_NAME,
        DEFAULT_PEERSCOUT_RECOMMEND_SCHEDULE
    )


# Note: need to save dag to a variable
with create_dag(
        dag_id=DAG_ID,
        schedule_interval=get_schedule_interval()) as dag:
    _ = (
        create_run_notebook_operator(
            notebook_filename='peerscout/peerscout-recommend-reviewing-editors.ipynb'
        )
        >> create_run_notebook_operator(
            notebook_filename='/'.join([
                'peerscout',
                'peerscout-update-manuscript-version-matching-reviewing-editor-profile.ipynb'
            ])
        )
    )
