import schedule
import time
from my_daily_task import delete_old_time_slots_and_dates, generate_time_slots_for_all_schedules


def run_daily_task():
    """
    Runs the daily task: delete old time slots and generate new ones.
    """
    print("Running daily task...")
    delete_old_time_slots_and_dates()
    generate_time_slots_for_all_schedules()


def schedule_task():
    """
    Schedules the task to run once a day.
    """
    # Schedule the task to run at 2:00 AM every day
    schedule.every().day.at("00:00").do(run_daily_task)

    # Run the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait for 1 minute before checking again


if __name__ == "__main__":
    schedule_task()
