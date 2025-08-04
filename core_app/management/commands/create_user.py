from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from core_app.models import UserProfile
from getpass import getpass


class Command(BaseCommand):
    help = 'Create a new user with specified role'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new user')
        parser.add_argument('--email', type=str, help='Email for the new user')
        parser.add_argument('--role', type=str, choices=['member', 'staff', 'admin'], 
                          default='member', help='Role for the user (default: member)')
        parser.add_argument('--first-name', type=str, help='First name')
        parser.add_argument('--last-name', type=str, help='Last name')
        parser.add_argument('--phone', type=str, help='Phone number')
        parser.add_argument('--company', type=str, help='Company name')
        parser.add_argument('--password', type=str, help='Password (will prompt if not provided)')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email'] or f'{username}@example.com'
        role = options['role']
        first_name = options['first_name'] or ''
        last_name = options['last_name'] or ''
        phone = options['phone'] or ''
        company = options['company'] or ''
        password = options['password']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            raise CommandError(f'User "{username}" already exists')

        # Get password if not provided
        if not password:
            password = getpass('Enter password: ')
            password_confirm = getpass('Confirm password: ')
            if password != password_confirm:
                raise CommandError('Passwords do not match')

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create user profile (will be created automatically by signal)
            # But we can update the role
            profile = user.userprofile
            profile.role = role
            profile.phone_number = phone
            profile.company_name = company
            profile.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created user "{username}" with role "{role}"'
                )
            )
            
            self.stdout.write(f'Username: {username}')
            self.stdout.write(f'Email: {email}')
            self.stdout.write(f'Role: {role}')
            if first_name or last_name:
                self.stdout.write(f'Name: {first_name} {last_name}'.strip())
            if phone:
                self.stdout.write(f'Phone: {phone}')
            if company:
                self.stdout.write(f'Company: {company}')

        except Exception as e:
            raise CommandError(f'Failed to create user: {str(e)}') 