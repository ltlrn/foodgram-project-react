from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.models import Tag
import logging


logger = logging.getLogger(__name__)


class TagViewSetTests(APITestCase):

    def add_test_tag(self):
        logger.debug('Adding a mock tag into database')

        tag = Tag(
            name='mockfast', 
            color='red', 
            slug='mockf'
        )
        tag.save()

        logger.debug('Successfully added mock tag into the database')

    def test_list_tags(self):
        """
        Test to list all the tags in the list
        """
        logger.debug('Starting test list tags')

        self.add_test_tag()

        url = 'http://localhost:8000%s'%reverse('tag-list')

        logger.debug('Sending TEST data to url: %s'%url)

        response = self.client.get(url, format='json')
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(json, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing result count')
        self.assertEqual(len(json), 5)