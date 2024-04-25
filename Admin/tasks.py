from celery import shared_task
from Admin.utils import set_attendance
from datetime import datetime, timedelta

@shared_task
def get_Attendance():
    now = datetime.now()
    current_day = now.strftime("%A").lower()
    current_time = now.time()

    if timedelta(hours=9) <= current_time <= timedelta(hours=17):
        if should_process_attendance():
            process_attendance()
        
def should_process_attendance():
    return True

def process_attendance():
    set_attendance(time=300)