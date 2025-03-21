import schedule

def job():
    print("Hello, World!")
# Then, you can schedule the job to run every minute using

schedule.every(5).minutes.do(job)