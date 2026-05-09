from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()


class NotificationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='notifuser', password='pass@123')
        self.other_user = User.objects.create_user(username='otheruser', password='pass@123')
        self.list_url = reverse('notifications:list')
        self.notif1 = Notification.objects.create(
            user=self.user, type='general', title='Test Notification',
            message='Hello!', is_read=False
        )
        self.notif2 = Notification.objects.create(
            user=self.user, type='application_update', title='App Update',
            message='Your app was reviewed.', is_read=True
        )
        self.other_notif = Notification.objects.create(
            user=self.other_user, type='general', title='Other User Notif',
            message='Not yours.', is_read=False
        )

    def test_list_renders(self):
        self.client.login(username='notifuser', password='pass@123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_mark_single_as_read(self):
        self.client.login(username='notifuser', password='pass@123')
        url = reverse('notifications:mark_read', args=[self.notif1.pk])
        self.client.post(url)
        self.notif1.refresh_from_db()
        self.assertTrue(self.notif1.is_read)

    def test_mark_all_as_read(self):
        self.client.login(username='notifuser', password='pass@123')
        url = reverse('notifications:mark_all_read')
        self.client.post(url)
        unread = Notification.objects.filter(user=self.user, is_read=False)
        self.assertEqual(unread.count(), 0)

    def test_delete_notification(self):
        self.client.login(username='notifuser', password='pass@123')
        count_before = Notification.objects.filter(user=self.user).count()
        url = reverse('notifications:delete', args=[self.notif1.pk])
        self.client.post(url)
        self.assertLess(Notification.objects.filter(user=self.user).count(), count_before)

    def test_filter_unread(self):
        self.client.login(username='notifuser', password='pass@123')
        response = self.client.get(self.list_url, {'filter': 'unread'})
        self.assertEqual(response.status_code, 200)
        notifs = response.context.get('notifications', [])
        for n in notifs:
            self.assertFalse(n.is_read)

    def test_cannot_delete_other_users_notification(self):
        self.client.login(username='notifuser', password='pass@123')
        url = reverse('notifications:delete', args=[self.other_notif.pk])
        response = self.client.post(url)
        self.assertIn(response.status_code, [403, 404, 302])
        self.assertTrue(Notification.objects.filter(pk=self.other_notif.pk).exists())

    def test_notifications_require_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)