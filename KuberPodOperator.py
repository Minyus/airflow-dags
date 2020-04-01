from airflow import DAG
from airflow.operators import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime, timedelta

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'manasi',
    'depends_on_past': False,
    'start_date': datetime(2016, 4, 15),
    'email': ['manasidalvi14@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('kubernetes_sample', default_args=default_args, schedule_interval=timedelta(minutes=10))

start = BashOperator(
    task_id='run_this_first',
    bash_command='echo "Hello World "',
    dag=dag)

passing = KubernetesPodOperator(
    namespace="default",
    image="Python:3.6",
    cmds=["Python", "-c"],
    arguments=["print('hello airflow')"],
    labels={'foo': 'bar'},
    name='passing-test',
    task_id='passing-task',
    get_logs=True,
    dag=dag,
)

failing = KubernetesPodOperator(
    namespace="default",
    image="Ubuntu:1604",
    cmds=["Python", "-c"],
    arguments=["print('hello world')"],
    labels={'foo': 'bar'},
    name='failing-test',
    task_id='failing-task',
    get_logs=True,
    dag=dag,
)

passing.set_upstream(start)
failing.set_upstream(start)
