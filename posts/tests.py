from django.contrib.auth.models import User 
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):

    def setUp(self):
        User.objects.create_user(username='holly', password='password')

    def test_can_list_posts(self):
        holly = User.objects.get(username='holly')
        Post.objects.create(owner=holly, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='holly', password='password')
        response = self.client.post('/posts/', {'title': 'this is a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'I am illegal'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):

    def setUp(self):
        holly = User.objects.create_user(username='holly', password='pass')
        daisy = User.objects.create_user(username='daisy', password='word')

        Post.objects.create(owner=holly, title='holly', content='daisy')
        Post.objects.create(owner=daisy, title='daisy', content='holly')

    def test_can_retrieve_post_with_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'holly')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_post_with_invalid_id(self):
        response = self.client.get('/posts/1382/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_can_update_own_posts(self):
        self.client.login(username='holly', password='pass')
        response = self.client.put('/posts/1/', {'title': 'new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_cannot_update_others_posts(self):
        self.client.login(username='holly', password='pass')
        response = self.client.put('/posts/2/', {'title': 'new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)