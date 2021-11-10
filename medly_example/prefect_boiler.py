from datetime import timedelta

from prefect import Client
from prefect.schedules import IntervalSchedule

from full_refresh import main_full_refresh as full_refresh_flow

client = Client()

project_name = "medly_example"

client.create_project(project_name=project_name)

daily_schedule = IntervalSchedule(interval=timedelta(days=1))
flow = full_refresh_flow()
flow.schedule = daily_schedule
flow.register(project_name=project_name)
