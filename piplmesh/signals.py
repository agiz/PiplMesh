from django import dispatch

from pushserver import signals

@dispatch.receiver(signals.passthrough)
def process_passthrough(sender, request, channel_id, action):
    print request.user, channel_id, action