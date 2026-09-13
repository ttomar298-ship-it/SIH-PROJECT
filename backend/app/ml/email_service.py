import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

class EmailAlertService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.sender_email = os.getenv("ALERT_SENDER_EMAIL", self.smtp_user or "alerts@sih26017.gov.in")
        self.recipient_email = os.getenv("ALERT_RECIPIENT_EMAIL", "district.collector@gov.in")

    def send_high_risk_alert(self, alert_data: Dict[str, Any], recipient: str = None) -> Dict[str, Any]:
        """
        Sends an email alert for high-risk projects.
        Falls back to simulation mode if SMTP credentials are not configured.
        """
        to_email = recipient or self.recipient_email
        project_id = alert_data.get("project_id", "N/A")
        project_name = alert_data.get("project_name", "N/A")
        risk_score = alert_data.get("risk_score", 0)
        severity = alert_data.get("severity", "CRITICAL")
        alert_msgs = alert_data.get("alert_messages", [])

        subject = f"[{severity} ALERT] SIH26017 Land Acquisition Delay Alert: {project_id} (Score: {risk_score}/100)"
        
        # Build HTML content
        messages_html = "".join([f"<li style='margin-bottom: 6px;'>{msg}</li>" for msg in alert_msgs])
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #1F2937;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #E5E7EB; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #DC2626; color: white; padding: 16px 24px;">
                    <h2 style="margin: 0; font-size: 20px;">🚨 SIH26017 High Risk Delay Alert</h2>
                </div>
                <div style="padding: 24px;">
                    <p style="font-size: 16px;">This is an automated priority notification from the <strong>Infrastructure Delay Prediction Engine</strong>.</p>
                    <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
                        <tr style="border-bottom: 1px solid #E5E7EB;">
                            <td style="padding: 8px 0; font-weight: bold;">Project ID:</td>
                            <td style="padding: 8px 0;">{project_id}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E5E7EB;">
                            <td style="padding: 8px 0; font-weight: bold;">Project Name:</td>
                            <td style="padding: 8px 0;">{project_name}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E5E7EB;">
                            <td style="padding: 8px 0; font-weight: bold;">State & District:</td>
                            <td style="padding: 8px 0;">{alert_data.get('district')}, {alert_data.get('state')}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E5E7EB;">
                            <td style="padding: 8px 0; font-weight: bold;">Calibrated Risk Score:</td>
                            <td style="padding: 8px 0; color: #DC2626; font-size: 18px; font-weight: bold;">{risk_score} / 100</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Severity Level:</td>
                            <td style="padding: 8px 0;"><span style="background-color: #FEE2E2; color: #991B1B; padding: 3px 8px; border-radius: 4px; font-weight: bold;">{severity}</span></td>
                        </tr>
                    </table>

                    <h4 style="margin-bottom: 8px; color: #374151;">Identified Bottlenecks:</h4>
                    <ul style="padding-left: 20px; color: #4B5563;">
                        {messages_html}
                    </ul>

                    <div style="background-color: #F3F4F6; padding: 12px 16px; border-radius: 6px; margin-top: 20px;">
                        <strong>Recommended Action:</strong> Coordinate with District Land Acquisition Officer and fast-track dispute resolution.
                    </div>
                </div>
                <div style="background-color: #F9FAFB; padding: 12px 24px; font-size: 12px; color: #6B7280; text-align: center;">
                    Smart India Hackathon SIH26017 Prototype • Automated Early Warning System
                </div>
            </div>
        </body>
        </html>
        """

        # If credentials are not set, return simulated dispatch
        if not self.smtp_user or not self.smtp_password:
            return {
                "status": "success",
                "mode": "simulated",
                "recipient": to_email,
                "subject": subject,
                "message": f"Simulated email alert dispatched for {project_id} to {to_email}",
                "html_preview": html_body
            }

        # Real SMTP delivery
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = to_email
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.sender_email, to_email, msg.as_string())

            return {
                "status": "success",
                "mode": "live_smtp",
                "recipient": to_email,
                "subject": subject,
                "message": f"Live email alert dispatched to {to_email}"
            }
        except Exception as e:
            return {
                "status": "error",
                "mode": "live_smtp",
                "recipient": to_email,
                "error": str(e),
                "message": f"SMTP dispatch failed: {str(e)}"
            }

_email_service_instance = None

def get_email_service() -> EmailAlertService:
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailAlertService()
    return _email_service_instance

