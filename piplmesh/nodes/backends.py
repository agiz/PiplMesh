from __future__ import absolute_import

import copy, random

from . import data, models

class RandomNodesBackend(object):
    def get_source_node(self, request):
        """
        Returns a node at random.
        """

        node_id = random.randrange(len(models.Node.objects()))
        node = copy.copy(models.Node.objects()[node_id])
        node.id = node_id
        return node

    def get_closest_node(self, request, latitude, longitude):
        """
        Because searching for real closest node is complex,
        it just returns a random node.
        """

        node_id = random.randrange(len(models.Node.objects()))
        node = copy.copy(models.Node.objects()[node_id])
        node.id = node_id
        return node

    def get_node(self, node_id):
        try:
            node = copy.copy(models.Node.objects()[node_id])
            node.id = node_id
            return node
        except IndexError:
            return None
