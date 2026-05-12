"""Goldlabel branded HTML email template."""

_LOGO_URL = "https://goldlabel.pro/shared/png/virus/virus.png"
_BASE_URL = "https://goldlabel.pro/virus"

# Palette (light theme only - light backgrounds with dark text)
_LIGHT_BG     = "#ffffff"
_LIGHT_PAPER  = "#ffffff"
_ACCENT_COLOR = "#ffd849"
_DARK_TEXT    = "#000000"
_LIGHT_TEXT   = "#666666"
_SECONDARY_BG = "#FFFFFF"


def goldlabel_email(
    subject: str,
    body_html: str,
    cta_label: str = "Call To Action",
    cta_url: str = _BASE_URL,
) -> str:
    """Return a complete HTML email string with Goldlabel branding.

    Args:
        subject:   Used as the visible heading inside the email.
        body_html: Inner HTML content placed in the message body area.
        cta_label: Label rendered in the full-width call-to-action button.
        cta_url:   Destination URL for the call-to-action button.

    Returns:
        A self-contained HTML string ready to pass to send_email_resend().
    """
    return f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="light dark" />
  <meta name="supported-color-schemes" content="light dark" />
  <title>{subject}</title>
  <style>
    /* ── Reset ─────────────────────────────────────── */
    body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
    table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
    img {{ -ms-interpolation-mode: bicubic; border: 0; outline: none; text-decoration: none; display: block; }}

    /* ── Base ──────────────────────────────────────── */
    body {{
      margin: 0; padding: 0;
      background-color: {_LIGHT_BG};
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: {_DARK_TEXT};
    }}

    /* ── Light theme only ──────────────────────── */
    .email-wrapper {{ background-color: {_LIGHT_BG}; }}
    .email-card {{ background-color: {_LIGHT_PAPER}; color: {_DARK_TEXT}; }}
    .email-header-inner {{ background-color: {_SECONDARY_BG}; }}
    .email-footer {{ background-color: {_SECONDARY_BG}; color: {_LIGHT_TEXT}; }}
    .email-subject {{ color: {_DARK_TEXT}; }}
    .email-cta {{ background-color: {_DARK_TEXT}; color: #ffffff; }}
    a {{ color: {_DARK_TEXT}; text-decoration: underline; }}
  </style>
</head>
<body class="email-wrapper">
  <!-- Outer wrapper -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
         style="padding: 0;">
    <tr>
      <td align="center">

        <!-- Card -->
        <table role="presentation" class="email-card" width="600" cellpadding="0" cellspacing="0"
               style="max-width:600px; width:100%; background-color:{_LIGHT_PAPER};
             border-radius:6px; overflow:hidden;
                      box-shadow:none;">

          <!-- Header -->
          <tr>
            <td class="email-header" align="center"
                style="padding:24px 40px 0 40px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="email-header-inner"
                     style="background-color:{_SECONDARY_BG}; border-radius:6px; max-width:300px; margin:0 auto;">
                <tr>
                  <td align="center" valign="middle" style="padding:20px;">
                    <a href="{_BASE_URL}" style="text-decoration:none; display:inline-block;">
                      <img src="{_LOGO_URL}"
                           width="48" height="48"
                           alt="Virus°"
                           style="width:48px; height:48px; border-radius:6px; display:block; margin:0 auto 10px auto;" />
                    </a>
                    <h1 class="email-subject"
                        style="margin:0; font-size:22px; font-weight:700;
                               color:{_DARK_TEXT}; line-height:1.3;">
                      {subject}
                    </h1>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td align="left"
                style="padding: 30px 40px 24px 40px;
                       font-size:15px; line-height:1.7; color:{_DARK_TEXT};">
              {body_html}
            </td>
          </tr>

          <!-- CTA -->
          <tr>
            <td align="center" style="padding: 0 40px 28px 40px;">
              <a class="email-cta"
                 href="{cta_url}"
                 style="display:inline-block;
                        background-color:{_DARK_TEXT}; color:#ffffff;
                        font-size:16px; font-weight:700; text-align:center;
                        text-decoration:none; border-radius:6px;
                        padding:14px 28px;">
                {cta_label}
              </a>
            </td>
          </tr>


          <!-- Footer -->
          <tr>
            <td class="email-footer" align="center"
                style="padding: 20px 40px;
                       font-size:12px; color:{_LIGHT_TEXT};
                       background-color:{_SECONDARY_BG};">
              <a href="https://github.com/goldlabelapps/python"
                 style="color:{_DARK_TEXT}; text-decoration:none;">
                 Sent with Python°
              </a>
             
            </td>
          </tr>

        </table>
        <!-- /Card -->

      </td>
    </tr>
  </table>
</body>
</html>"""
