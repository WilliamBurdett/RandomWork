from datetime import timedelta, datetime

from prefect import Client
from prefect.executors import LocalDaskExecutor
from prefect.schedules import IntervalSchedule

from full_refresh import main_full_refresh as full_refresh_flow

client = Client()

project_name = "medly_example"

client.create_project(project_name=project_name)

start_time = datetime.now().replace(hour=22, minute=15, second=0, microsecond=0)
daily_schedule = IntervalSchedule(start_date=start_time, interval=timedelta(days=1))
flow = full_refresh_flow()
flow.executor = LocalDaskExecutor(scheduler="threads", num_workers=2)
flow.schedule = daily_schedule
flow.register(project_name=project_name)
