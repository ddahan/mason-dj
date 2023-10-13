from smtplib import SMTPException

from django.core import mail
from django.core.mail.message import EmailMessage
from django.db import models
from django.template import Template
from django.template.context import Context

from core.mixins.slugable import Slugable

from ..exceptions import MailSlugNotFound
from ..parameters import contact_emitter


class ItemFlavour(models.TextChoices):
    TO = "to"
    BCC = "bcc"


class MailSkeleton(Slugable, models.Model):
    subject = models.CharField(max_length=998)
    html_body = models.TextField()
    send_mode = models.CharField(max_length=512, choices=ItemFlavour.choices)

    class Meta:
        db_table = "tb_mail_datas"

    def __str__(self):
        return self.slug

    @classmethod
    def send_with(cls, slug, recipients_and_contexts: dict) -> tuple[bool, int | None]:
        """Shortcut to send method without requiring to get the object first"""
        try:
            mail_data = cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            raise MailSlugNotFound()
        else:
            return mail_data.send(recipients_and_contexts)

    def send(self, recipients_and_contexts: dict) -> tuple[bool, int | None]:
        """
        Send an email to a single or multiple users
        :param recipients_and_contexts: a dictionnary where key is <email> and value is
         <context> (note that <context> can be None)
        :return: a tuple containing an error boolean and an optional integer to indicate
        the number of mails sent.
        # TODO: use as a background Celery task
        """

        email_messages = []
        for recipient, context_dict in recipients_and_contexts.items():
            template = Template(self.html_body)
            context = Context(context_dict)
            msg = EmailMessage(
                subject=self.subject,
                body=template.render(context),
                from_email=contact_emitter.pretty_display(),
            )
            setattr(msg, self.send_mode, [recipient])  # shortcut
            msg.content_subtype = "html"  # Main content is now text/html
            email_messages.append(msg)

        connection = mail.get_connection()  # Use default email connection
        try:
            nb_mails_sent = connection.send_messages(email_messages)
        except SMTPException:
            return (False, None)  # FIXME: log error
        except Exception:
            return (False, None)  # FIXME: log error
        else:
            return (True, nb_mails_sent)  # FIXME: log success
