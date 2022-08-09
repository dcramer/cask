from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from cask.accounts.models import User
from cask.accounts.utils import generate_token


class Command(BaseCommand):
    help = "Generate an authentication token for the given user"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(email=options["email"])

        expires_in = 3600 * 24 * 30

        token = generate_token(user, expires_in)

        self.stdout.write(
            self.style.MIGRATE_HEADING('Authentication for "%s"' % user.email)
        )
        self.stdout.write(self.style.SQL_FIELD("User ID"))
        self.stdout.write(self.style.MIGRATE_LABEL("  %s " % str(user.id)))
        self.stdout.write(self.style.SQL_FIELD("Email"))
        self.stdout.write(self.style.MIGRATE_LABEL("  %s " % user.email))
        self.stdout.write(self.style.SQL_FIELD("Token"))
        self.stdout.write(self.style.MIGRATE_LABEL("  %s " % token))
        self.stdout.write(self.style.SQL_FIELD("Expires"))
        self.stdout.write(
            self.style.MIGRATE_LABEL(
                "  %s" % str((timezone.now() + timedelta(minutes=expires_in)))
            )
        )
