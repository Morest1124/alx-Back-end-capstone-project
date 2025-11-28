from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading

class EmailService:
    """
    Service for sending automated email notifications.
    Uses threading to send emails asynchronously to avoid blocking the request.
    """
    
    @staticmethod
    def send_async_email(subject, message, recipient_list, html_message=None):
        """Helper to send email in a separate thread"""
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=True
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

    @classmethod
    def send_proposal_accepted_email(cls, proposal):
        """Notify freelancer that their proposal was accepted"""
        subject = f"Proposal Accepted: {proposal.project.title}"
        recipient = proposal.freelancer.email
        
        message = f"""
        Hi {proposal.freelancer.first_name},
        
        Congratulations! Your proposal for "{proposal.project.title}" has been accepted by {proposal.project.client.first_name}.
        
        Project Budget: ${proposal.price}
        Status: In Progress
        
        A payment of ${proposal.price} has been held in escrow and will be released upon completion.
        
        You can now start working on the project.
        
        Good luck!
        The BinaryBlade24 Team
        """
        
        threading.Thread(
            target=cls.send_async_email,
            args=(subject, message, [recipient])
        ).start()

    @classmethod
    def send_payment_released_email(cls, project, amount):
        """Notify freelancer that payment has been released"""
        # Find the freelancer (assuming one active proposal)
        proposal = project.proposals.filter(status='ACCEPTED').first()
        if not proposal:
            return
            
        recipient = proposal.freelancer.email
        subject = f"Payment Released: {project.title}"
        
        message = f"""
        Hi {proposal.freelancer.first_name},
        
        Great news! The client has approved your work for "{project.title}".
        
        A payment of ${amount} has been released from escrow to your account.
        
        Thank you for your hard work!
        The BinaryBlade24 Team
        """
        
        threading.Thread(
            target=cls.send_async_email,
            args=(subject, message, [recipient])
        ).start()

    @classmethod
    def send_new_message_email(cls, message_obj):
        """Notify user of a new message"""
        recipient = message_obj.conversation.get_other_participant(message_obj.sender)
        subject = f"New Message from {message_obj.sender.first_name}"
        
        body = f"""
        Hi {recipient.first_name},
        
        You have received a new message from {message_obj.sender.first_name} regarding "{message_obj.conversation.project.title}".
        
        "{message_obj.body[:100]}..."
        
        Log in to view the full message and reply.
        
        The BinaryBlade24 Team
        """
        
        threading.Thread(
            target=cls.send_async_email,
            args=(subject, body, [recipient.email])
        ).start()
