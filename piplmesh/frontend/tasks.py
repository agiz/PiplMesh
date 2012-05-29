import datetime, json, urllib

from django.conf import settings

from celery import task

from pushserver.utils import updates

from piplmesh.account import models
from piplmesh.nodes import data, models as node_models
from piplmesh.frontend import views

CHECK_ONLINE_USERS_RECONNECT_TIMEOUT = 2 * settings.CHECK_ONLINE_USERS_INTERVAL

@task.task
def check_online_users():
    for user in models.User.objects(
        is_online=False,
        connections__not__in=([], None), # None if field is missing altogether, not__in seems not to be equal to nin
    ):
        if models.User.objects(
            pk=user.pk,
            is_online=False,
            connections__not__in=([], None), # None if field is missing altogether, not__in seems not to be equal to nin
        ).update(set__is_online=True):
            updates.send_update(
                views.HOME_CHANNEL_ID,
                {
                    'type': 'userlist',
                    'action': 'JOIN',
                    'user': {
                        'username': user.username,
                        'profile_url': user.get_profile_url(),
                        'image_url': user.get_image_url(),
                    },
                }
            )

    for user in models.User.objects(
        is_online=True,
        connections__in=([], None), # None if field is missing altogether
        connection_last_unsubscribe__lt=datetime.datetime.now() - datetime.timedelta(seconds=CHECK_ONLINE_USERS_RECONNECT_TIMEOUT),
    ):
        if models.User.objects(
            pk=user.pk,
            is_online=True,
            connections__in=([], None), # None if field is missing altogether
            connection_last_unsubscribe__lt=datetime.datetime.now() - datetime.timedelta(seconds=CHECK_ONLINE_USERS_RECONNECT_TIMEOUT),
        ).update(set__is_online=False):
            updates.send_update(
                views.HOME_CHANNEL_ID,
                {
                    'type': 'userlist',
                    'action': 'PART',
                    'user': {
                        'username': user.username,
                        'profile_url': user.get_profile_url(),
                        'image_url': user.get_image_url(),
                    },
                }
            )

@task.task
def update_nodes():
    # TODO: unique, constant node_id
    for node in data.nodes:
        retnode, created = node_models.Node.objects.get_or_create(
            id=node.name,
            name=node.name,
            address=node.address.decode('utf-8'),
            location=node.location,
            url=node.url,
        )

@task.task
def update_venues():
    # TODO: Remove enumerate and break
    for i, node in enumerate(node_models.Node.objects()):
        start = datetime.datetime.now()
        node_data = urllib.urlopen("http://odpiralnicasi.com/spots.json?lat=%s&lng=%s" % (node.location[0], node.location[1]))
        node_venues = json.load(node_data)
        for venue in node_venues['spots']:
            # TODO: How long is venue still open?
            address = ''
            if 'full_address' in venue:
                address = venue['full_address']
            elif 'street' in venue and 'city' in venue:
                address = venue['street']+', '+venue['city']
                
            distance = ''
            if 'distance' in venue:
                distance = venue['distance']

            location = node.location
            if 'lat' in venue and 'lng' in venue:
                location = [venue['lat'], venue['lng']]
                
            name = ''
            if 'combined_name' in venue:
                name = venue['combined_name']
            elif 'company' in venue and 'name' in venue:
                name = venue['company']+' '+venue['name']
            elif 'company' in venue:
                name = venue['company']
            elif 'name' in venue:
                name = venue['name']

            is_open = False
            if 'is_open' in venue:
                is_open = venue['is_open']
            
            open_hours = {}
            if 'open_mon' in venue:
                open_hours['open_mon'] = venue['open_mon']
            if 'open_tue' in venue:
                open_hours['open_tue'] = venue['open_tue']
            if 'open_wed' in venue:
                open_hours['open_wed'] = venue['open_wed']
            if 'open_thu' in venue:
                open_hours['open_thu'] = venue['open_thu']
            if 'open_fri' in venue:
                open_hours['open_fri'] = venue['open_fri']
            if 'open_sat' in venue:
                open_hours['open_sat'] = venue['open_sat']
            if 'open_sun' in venue:
                open_hours['open_sun'] = venue['open_sun']

            tmp = node_models.OCVenue(
                oc_node=node.id,
                oc_address=address,
                oc_distance=distance,
                oc_location=location,
                oc_name=name,
                oc_is_open=is_open,
                oc_timeleft='',
                oc_open_hours=open_hours,
                oc_extra=[],
                oc_last_update=datetime.datetime.now(),
            )
            tmp.save()

        node_models.OCVenue.objects(
            oc_node=node.id,
            oc_last_update__lt=start,
        ).delete()

        if i >= 0:
            break
