import urlparse

from django.core import urlresolvers
from django.test import client, utils
from django.utils import simplejson as json

from piplmesh import test_runner
from piplmesh.account import models as account_models

@utils.override_settings(DEBUG=True)
class BasicTest(test_runner.MongoEngineTestCase):
    api_name = 'v1'
    user_username = 'test_user'
    user_password = 'foobar'

    def setUp(self):
        account_models.User.create_user(self.user_username, self.user_password)

        self.client = client.Client()
        self.client.login(username=self.user_username, password=self.user_password)

    def resourceListURI(self, resource_name):
        return urlresolvers.reverse('api_dispatch_list', kwargs={'api_name': self.api_name, 'resource_name': resource_name})

    def resourcePK(self, resource_uri):
        match = urlresolvers.resolve(resource_uri)
        return match.kwargs['pk']

    def resourceDetailURI(self, resource_name, resource_pk):
        return urlresolvers.reverse('api_dispatch_detail', kwargs={'api_name': self.api_name, 'resource_name': resource_name, 'pk': resource_pk})

    def fullURItoAbsoluteURI(self, uri):
        scheme, netloc, path, query, fragment = urlparse.urlsplit(uri)
        return urlparse.urlunsplit((None, None, path, query, fragment))

    def test_basic(self):
        # Creating a post

        response = self.client.post(self.resourceListURI('post'), '{"message": "Test post."}', content_type='application/json')
        self.assertEqual(response.status_code, 201)

        post_uri = response['location']

        response = self.client.get(post_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['message'], 'Test post.')
        self.assertEqual(response['author']['username'], self.user_username)
        self.assertNotEqual(response['created_time'], None)
        self.assertNotEqual(response['updated_time'], None)
        self.assertEqual(response['comments'], [])
        self.assertEqual(response['attachments'], [])

        post_created_time = response['created_time']
        post_updated_time = response['updated_time']

        # Adding an attachment

        attachments_resource_uri = self.fullURItoAbsoluteURI(post_uri) + 'attachments/'

        response = self.client.post(attachments_resource_uri, '{"link_url": "http://wlan-si.net/", "link_caption": "wlan slovenija"}', content_type='application/json; type=link')
        self.assertEqual(response.status_code, 201)

        attachment_uri = response['location']

        response = self.client.get(attachment_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['link_url'], 'http://wlan-si.net/')
        self.assertEqual(response['link_caption'], 'wlan slovenija')
        self.assertEqual(response['link_description'], '')
        self.assertEqual(response['author']['username'], self.user_username)

        response = self.client.get(post_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['attachments'][0]['link_url'], 'http://wlan-si.net/')
        self.assertEqual(response['attachments'][0]['link_caption'], 'wlan slovenija')
        self.assertEqual(response['attachments'][0]['link_description'], '')
        self.assertEqual(response['created_time'], post_created_time)
        self.assertNotEqual(response['updated_time'], post_updated_time)

        post_updated_time = response['updated_time']

        # Adding a comment

        comments_resource_uri = self.fullURItoAbsoluteURI(post_uri) + 'comments/'

        response = self.client.post(comments_resource_uri, '{"message": "Test comment."}', content_type='application/json')
        self.assertEqual(response.status_code, 201)

        comment_uri = response['location']

        response = self.client.get(comment_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['message'], 'Test comment.')
        self.assertEqual(response['author']['username'], self.user_username)

        response = self.client.get(post_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['comments'][0], self.fullURItoAbsoluteURI(comment_uri))
        self.assertEqual(response['created_time'], post_created_time)
        self.assertNotEqual(response['updated_time'], post_updated_time)