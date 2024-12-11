import schedule
import time
from my_daily_task import delete_old_time_slots_and_dates, generate_time_slots_for_all_schedules


def run_daily_task():
    print("Running daily task...")
    delete_old_time_slots_and_dates()
    generate_time_slots_for_all_schedules()


def schedule_task():
    schedule.every().day.at("00:00").do(run_daily_task)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    schedule_task()
