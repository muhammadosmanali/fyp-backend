import os
from typing import List
from requests import Response, post
from libs.strings import gettext


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    MAILGUN_API_KEY = "65501758c933c6c5f818c4c3d34d3bc7-074fa10c-6b7b96e8"
    MAILGUN_DOMAIN = "sandbox3002964ec6fd434a909bc6cde8d6608e.mailgun.org"

    FROM_TITLE = "PLANTLET REGISTRATION"
    FROM_EMAIL = f"do-not-reply@{MAILGUN_DOMAIN}"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(gettext("mailgun_failed_load_api_key"))

        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(gettext("mailgun_failed_load_domain"))

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
        if response.status_code != 200:
            # print(response.status_code)
            # print(response.json())
            raise MailGunException(gettext("mailgun_error_send_email"))
        return response
