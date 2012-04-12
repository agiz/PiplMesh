import datetime

from celery.task import task

from piplmesh.account import models

@task
def add(x, y):
    # TODO: Implement logic, look for last message on the channel and deduct state.
    print "tasks add"
    chan_users = models.User.objects(lastaccess__gt=datetime.datetime.now() - datetime.timedelta(10))
    for user in chan_users:
        #print user.channel
        for c in user.channel:
            print c, user.channel[c], datetime.datetime.now() - datetime.timedelta(seconds=30), user.lastaccess, datetime.datetime.now()
            # if (user.lastaccess > user.channel[c] + datetime.timedelta(seconds=30)) or ():
            #if user.lastaccess > user.channel[c] + datetime.timedelta(seconds=30):
            if user.lastaccess > user.channel[c] and user.lastaccess + datetime.timedelta(seconds=30) < datetime.datetime.now():
                print c, "log out..."
                # TODO: Remove user last access time
                
    #print chan_users
    #add.apply_async(args=[1,2], countdown=10)
    return x + y

"""
from celery.task import Task

class RevokeableTask(Task):
#     Task that can be revoked.
# 
#     Example usage:
# 
#         @task(base=RevokeableTask)
#         def mytask():
#             pass
    

    def __call__(self, *args, **kwargs):
        if revoke_flag_set_in_db_for(self.request.id):
            return
        super(RevokeableTask, self).__call__(*args, **kwargs)
"""

#print "lol"
#add.apply_async(args=[1,2], countdown=10)