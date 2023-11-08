import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from reporter.models import Project, Task

fake = Faker()

class Command(BaseCommand):
    help = 'Populate your models with fake data'

    def handle(self, *args, **options):
        self.stdout.write('Populating your models with fake data...')

        #Generate fake data for Project model
        # for _ in range(10):  # Adjust the number of projects you want
        #     Project.objects.create(
        #         name=fake.company(),
        #         description=fake.text(max_nb_chars=200),
        #         created_at=timezone.now(),
        #         status=random.choice(['Active', 'Draft', 'Completed']),
        #         cost=random.randint(5, 300) * 100
        #     )

       # Generate fake data for Task model
        for _ in range(60):  # Adjust the number of tasks you want
            Task.objects.create(
                name=fake.job(),
                user_id=random.randint(1,2),  # Adjust the range based on your User IDs
                project_id=random.randint(52, 71),  # Adjust the range based on your Project IDs
                status=random.choice(['To Do', 'In Progress', 'Done', 'Cancelled']),
                created_at=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS('Fake data has been populated!'))
