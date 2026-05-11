"""Email notification routes."""

import os
import resend
from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr

from app.utils.make_meta import make_meta
from app.utils.email_templates import goldlabel_email

resend.api_key = os.environ.get("RESEND_API_KEY")
RESEND_API_KEY = resend.api_key

router = APIRouter(prefix="/notify")

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    html: str
    cta_label: str | None = None
    cta_url: str | None = None


def send_email_resend(to: str, subject: str, html: str) -> dict:
    if not resend.api_key:
        return {"error": "Missing RESEND_API_KEY"}
    params: resend.Emails.SendParams = {
        "from": "NX° <nx@goldlabel.pro>",
        "to": [to],
        "subject": subject,
        "html": html,
    }
    try:
        email: resend.Emails.SendResponse = resend.Emails.send(params)
        return dict(email)
    except Exception as e:
        return {"error": str(e)}


@router.get("/email")
def root() -> dict:
    """GET /notify/email endpoint."""
    if not RESEND_API_KEY:
        meta = make_meta("error", "RESEND_API_KEY is missing from environment. Please set it in your .env file.")
        return {"meta": meta}
    meta = make_meta("success", "GET /notify/email endpoint")
    return {
        "meta": meta,
        "data": {
            "hint": "Use POST /notify/email to send an email via Resend API.",
            "type": {
                "to": {
                    "type": "string",
                    "format": "email",
                    "required": True,
                    "description": "Recipient email address."
                },
                "subject": {
                    "type": "string",
                    "required": True,
                    "description": "Subject of the email."
                },
                "html": {
                    "type": "string",
                    "required": True,
                    "description": "HTML content of the email."
                },
                "cta_label": {
                    "type": "string",
                    "required": False,
                    "description": "Optional CTA button label. Defaults to 'Call To Action'."
                },
                "cta_url": {
                    "type": "string",
                    "required": False,
                    "description": "Optional CTA URL. Defaults to the website base URL."
                }
            }
        }
    }


@router.post("/email", status_code=status.HTTP_202_ACCEPTED)
def send_email(request: EmailRequest):
    """POST /notify/email endpoint to send email via Resend API."""
    if not RESEND_API_KEY:
        meta = make_meta("error", "RESEND_API_KEY missing. Please set it in your .env file.")
        return {"meta": meta}

    result = send_email_resend(
        to=request.to,
        subject=request.subject,
        html=goldlabel_email(
            request.subject,
            request.html,
            cta_label=request.cta_label or "Call To Action",
            cta_url=request.cta_url or "https://goldlabel.pro",
        ),
    )
    if "error" in result:
        meta = make_meta("error", result["error"])
        return {"meta": meta}

    meta = make_meta("success", "Email sent successfully.")
    return {"meta": meta, "data": result}
