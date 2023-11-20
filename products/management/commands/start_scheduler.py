import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from products.models import Order

logger = logging.getLogger(__name__)


def log_and_print(message):
    logger.info(message)
    print(message)


def send_payment_notification_emails():
    tomorrow = timezone.now().date() + timezone.timedelta(days=1)
    i = 0
    for order in Order.objects.all():
        if tomorrow <= order.payment_to:
            i += 1
            order.send_remainder_mail()

    log_and_print(
        BaseCommand().style.SUCCESS(
            f"Successfully sent emails ({i}) for day:{tomorrow}"
        )
    )


class Command(BaseCommand):
    help = "Fill database tables related for products application"

    def handle(self, *args, **options):
        if not settings.SEND_PAYMENT_REMAINDER_EMAILS:
            log_and_print("Scheduler is not enabled. Check .env file.")

        else:
            due_date = timezone.now().date() + timezone.timedelta(days=1)

            self.stdout.write(
                "Preparing to send remainder emails for due date: %s" % due_date
            )
            scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
            scheduler.add_job(
                send_payment_notification_emails,
                trigger=CronTrigger(hour="*", minute="*"),
                id="send_payment_notification_emails",
                max_instances=1,
                replace_existing=True,
            )
            log_and_print("Added job 'send_payment_notification_emails'.")
            try:
                log_and_print("Starting scheduler...")
                scheduler.start()
            except KeyboardInterrupt:
                log_and_print("Stopping scheduler...")
                scheduler.shutdown()
                log_and_print("Scheduler shut down successfully!")
