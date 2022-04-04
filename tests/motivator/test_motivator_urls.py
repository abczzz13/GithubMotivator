from django.urls import reverse, resolve


class TestMotivatorUrls:

    def test_goal_list(self):
        path = reverse('goal-list')

        assert resolve(path).view_name == 'goal-list'

    def test_goal_details(self):
        path = reverse('goal-detail', kwargs={'pk': 1})

        assert resolve(path).view_name == 'goal-detail'

    def test_goal_create(self):
        path = reverse('goal-create')

        assert resolve(path).view_name == 'goal-create'
