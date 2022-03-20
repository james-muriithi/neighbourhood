import email
from unicodedata import name
from django.test import TestCase
from app.models import Business, Contact, User, Post, Location,  NeighbourHood

# Create your tests here.


class PostTestClass(TestCase):  # Project class test
    def setUp(self):
        location = Location(
            name='Nairobi'
        )

        location.save_location()

        hood = NeighbourHood(
            name="example neighbourhood",
            location_id=location.id,
        )

        hood.save()

        # create a user
        user = User.objects.create(
            username="john", full_name="john doe", email="m@.com",
            location_id=location.id, neighbourhood_id=hood.id
        )

        hood.admin_id = user.id
        hood.save()
        user.save()

        self.post = Post(
            title="Test Project",
            content="Test Description",
            image="image.jpg",
            user=user,
            neighbourhood_id=hood.id,
            location_id=location.id,
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_save_method(self):
        self.post.save_post()
        post = Post.find_post(self.post.id)
        self.assertIsNotNone(post)

    def test_update_method(self):
        self.post.title = 'new title'
        self.post.save_post()
        post = Post.find_post(self.post.id)
        self.assertEqual(self.post.title, post.title)

    def test_delete_method(self):
        self.post.save_post()
        self.post.delete_post()
        post = Post.objects.filter(id=self.post.id).exists()
        self.assertFalse(post)


class NeighbourhoodTestClass(TestCase):  # Neighbourhood class test
    def setUp(self):
        location = Location(
            name='Nairobi'
        )

        location.save_location()

        # create a user
        user = User.objects.create(
            username="john", full_name="john doe", email="m@.com",
            location_id=location.id
        )

        user.save()

        self.hood = NeighbourHood(
            name="example neighbourhood",
            location=location,
            admin=user
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.hood, NeighbourHood))

    def test_save_method(self):
        self.hood.create_neigborhood()
        hood = NeighbourHood.find_neigborhood(self.hood.id)
        self.assertIsNotNone(hood)

    def test_update_method(self):
        self.hood.name = 'new name'
        self.hood.save()
        hood = NeighbourHood.find_neigborhood(self.hood.id)
        self.assertEqual(self.hood.name, hood.name)

    def test_delete_method(self):
        self.hood.create_neigborhood()
        self.hood.delete_neighbourhood()
        hood = NeighbourHood.objects.filter(id=self.hood.id).exists()
        self.assertFalse(hood)


# Location Model Tests
class LocationTestClass(TestCase):
    def setUp(self):
        self.location = Location(name='Test Location')

    def test_instance(self):
        self.assertTrue(isinstance(self.location, Location))

    def test_save_method(self):
        self.location.save_location()
        location = Location.get_location(self.location.id)
        self.assertIsNotNone(location)

    def test_delete_method(self):
        self.location.save_location()
        self.location.delete()
        locations = Location.objects.all()
        self.assertTrue(len(locations) == 0)


# Contact Model Tests
class ContactTestClass(TestCase):
    def setUp(self):
        location = Location(name='Test Location')
        location.save_location()

        user = User.objects.create(
            username="john", full_name="john doe", email="m@.com",
            location_id=location.id
        )

        user.save()

        hood = NeighbourHood(
            name="example neighbourhood",
            location=location,
            admin=user
        )
        hood.create_neigborhood()

        self.contact = Contact(
            name="police",
            email="",
            phone="123",
            neighbourhood=hood
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.contact, Contact))

    def test_save_method(self):
        self.contact.create_contact()
        contact = Contact.get_contact(self.contact.id)
        self.assertIsNotNone(contact)

    def test_delete_method(self):
        self.contact.create_contact()
        self.contact.delete()
        contact = Contact.objects.filter(id=self.contact.id).exists()
        self.assertFalse(contact)


# Contact Model Tests
class BusinessTestClass(TestCase):
    def setUp(self):
        location = Location(name='Test Location')
        location.save_location()

        user = User.objects.create(
            username="john", full_name="john doe", email="m@.com",
            location_id=location.id
        )

        user.save()

        hood = NeighbourHood(
            name="example neighbourhood",
            location=location,
            admin=user
        )
        hood.create_neigborhood()

        self.business = Business(
            name="test biz",
            user=user,
            neighbourhood=hood,
            email="m@a.com"
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.business, Business))

    def test_save_method(self):
        self.business.save_business()
        business = Business.get_business(self.business.id)
        self.assertIsNotNone(business)

    def test_delete_method(self):
        self.business.save_business()
        self.business.delete()
        business = Business.objects.filter(id=self.business.id).exists()
        self.assertFalse(business)