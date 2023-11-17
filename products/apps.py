import logging

from apscheduler.triggers.cron import CronTrigger
from django.apps import AppConfig
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler

from products.utils import send_payment_notification_emails

logger = logging.getLogger(__name__)


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        import products.signals

        if settings.SEND_PAYMENT_REMAINDER_EMAILS:
            scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
            scheduler.add_job(
                send_payment_notification_emails,
                trigger=CronTrigger(second="*/10"),  # Every 10 seconds
                id="send_payment_notification_emails",
                max_instances=1,
                replace_existing=True,
            )
            logger.info("Added job 'my_job'.")
            try:
                logger.info("Starting scheduler...")
                scheduler.start()
            except KeyboardInterrupt:
                logger.info("Stopping scheduler...")
                scheduler.shutdown()
                logger.info("Scheduler shut down successfully!")