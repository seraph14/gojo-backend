from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'backend.cron.MyCronJob'    # a unique code

    def do(self):
        pass    # do your thing here
        print("running ")