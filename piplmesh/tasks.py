import datetime

from celery.task import task

from pushserver.utils import updates

from piplmesh.account import models

@task
def prune_users():
    chan_users = models.User.objects()
    for user in chan_users:
        if len(user.opened_connections) == 0 and user.last_access and datetime.datetime.now() > user.last_access + datetime.timedelta(seconds=30):
            # TODO: Implement joining/parting subsystem
            user.update(
                set__opened_connections = [],
                unset__last_access = 1,
                set__channel = {},
            )

            channel_id = 'a'

            updates.send_update(
                channel_id,
                {
                    'type': 'answer',
                    'value': {
                        'action': 'PART',
                        'message': user.username
                    }
                }
            )