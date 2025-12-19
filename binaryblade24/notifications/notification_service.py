"""
Notification Service

Central service for creating and managing notifications.
Handles creation of in-app notifications and integration with email service.
"""

from .models import Notification
from .email_service import EmailService


class NotificationService:
    """
    Service for creating notifications across the platform.
    
    This service provides methods to create notifications for various events,
    and integrates with the email service to send emails when appropriate.
    """
    
    @classmethod
    def create_notification(cls, recipient, notification_type, title, message, 
                           project=None, proposal=None, order=None, link_url=''):
        """
        Create an in-app notification.
        
        Args:
            recipient: User who will receive the notification
            notification_type: Type from Notification.NOTIFICATION_TYPES
            title: Notification title
            message: Notification message
            project: Optional related project
            proposal: Optional related proposal
            order: Optional related order
            link_url: Optional URL to navigate to on click
            
        Returns:
            Created Notification object
        """
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            project=project,
            proposal=proposal,
            order=order,
            link_url=link_url
        )
        return notification
    
    @classmethod
    def notify_proposal_submitted(cls, proposal):
        """
        Notify client when a freelancer submits a proposal.
        
        Args:
            proposal: Proposal object that was submitted
        """
        cls.create_notification(
            recipient=proposal.project.client,
            notification_type='PROPOSAL_SUBMITTED',
            title=f"New Proposal on {proposal.project.title}",
            message=f"{proposal.freelancer.first_name} {proposal.freelancer.last_name} submitted a proposal for ${proposal.bid_amount}",
            project=proposal.project,
            proposal=proposal,
            link_url=f'/client/proposals?project={proposal.project.id}'
        )
    
    @classmethod
    def notify_proposal_accepted(cls, proposal):
        """
        Notify freelancer when their proposal is accepted.
        
        Args:
            proposal: Proposal object that was accepted
            
        Returns:
            Created Notification object
        """
        notification = cls.create_notification(
            recipient=proposal.freelancer,
            notification_type='PROPOSAL_ACCEPTED',
            title=f"Proposal Accepted: {proposal.project.title}",
            message=f"Congratulations! Your proposal was accepted by {proposal.project.client.first_name}.",
            project=proposal.project,
            proposal=proposal,
            link_url=f'/freelancer/projects/{proposal.project.id}'
        )
        
        # Also send email if preference enabled
        try:
            if hasattr(proposal.freelancer, 'notification_preferences'):
                if proposal.freelancer.notification_preferences.email_proposal_submitted:
                    EmailService.send_proposal_accepted_email(proposal)
        except Exception as e:
            print(f"Failed to send proposal accepted email: {e}")
        
        return notification
    
    @classmethod
    def notify_proposal_rejected(cls, proposal):
        """
        Notify freelancer when their proposal is rejected.
        
        Args:
            proposal: Proposal object that was rejected
        """
        cls.create_notification(
            recipient=proposal.freelancer,
            notification_type='PROPOSAL_REJECTED',
            title=f"Proposal Update: {proposal.project.title}",
            message=f"Your proposal for {proposal.project.title} was not selected this time.",
            project=proposal.project,
            proposal=proposal,
            link_url=f'/freelancer/proposals'
        )
    
    @classmethod
    def notify_message_received(cls, message):
        """
        Notify user when they receive a new message.
        
        Args:
            message: Message object that was sent
        """
        recipient = message.conversation.get_other_participant(message.sender)
        
        cls.create_notification(
            recipient=recipient,
            notification_type='MESSAGE_RECEIVED',
            title=f"New message from {message.sender.first_name}",
            message=message.body[:100] + ('...' if len(message.body) > 100 else ''),
            project=message.conversation.project if hasattr(message.conversation, 'project') else None,
            link_url=f'/messages?conversation={message.conversation.id}'
        )
        
        # Send email if enabled
        try:
            if hasattr(recipient, 'notification_preferences'):
                if recipient.notification_preferences.email_new_message:
                    EmailService.send_new_message_email(message)
        except Exception as e:
            print(f"Failed to send new message email: {e}")
    
    @classmethod
    def notify_payment_released(cls, project, amount, freelancer):
        """
        Notify freelancer when payment is released.
        
        Args:
            project: Project for which payment was released
            amount: Payment amount
            freelancer: Freelancer receiving payment
        """
        cls.create_notification(
            recipient=freelancer,
            notification_type='PAYMENT_RELEASED',
            title=f"Payment Released: {project.title}",
            message=f"Payment of ${amount} has been released for your work on {project.title}.",
            project=project,
            link_url=f'/freelancer/projects/{project.id}'
        )
        
        # Send email
        EmailService.send_payment_released_email(project, amount)
    
    @classmethod
    def notify_order_created(cls, order):
        """
        Notify freelancer when client creates an order for their gig.
        
        Args:
            order: Order object that was created
        """
        # Get the freelancer from the order items
        for item in order.items.all():
            freelancer = item.freelancer
            cls.create_notification(
                recipient=freelancer,
                notification_type='ORDER_CREATED',
                title=f"New Order: {item.project.title}",
                message=f"{order.client.first_name} purchased your {item.get_tier_display()} package for ${item.price}.",
                project=item.project,
                order=order,
                link_url=f'/freelancer/orders/{order.id}'
            )
    
    @classmethod
    def notify_review_received(cls, review):
        """
        Notify user when they receive a review.
        
        Args:
            review: Review object that was created
        """
        cls.create_notification(
            recipient=review.reviewee,
            notification_type='REVIEW_RECEIVED',
            title=f"New Review from {review.reviewer.first_name}",
            message=f"You received a {review.rating}-star review on {review.project.title}.",
            project=review.project,
            link_url=f'/profile/{review.reviewee.id}'
        )
