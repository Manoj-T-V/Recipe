# recipe/tasks.py
from celery import shared_task
import logging
import smtplib, ssl
from django.core.mail import send_mail
from django.utils import timezone
from .models import Recipe, RecipeLike
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
print(project_root)
# Ensure Django settings are configured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

@shared_task
def notify_author_about_likes():
    logger.info('Function started')
    subject = 'Recipe Like Notification'
    message = f'Your recipe with ID  has received new likes!'
    from_email = 'manoj.venkateshgowda@campusuvce.in'
    recipient_list = ['manojtvmtv@gmail.com'] 
    try:
        print('sending email')
        send_mail(subject, message, from_email, recipient_list)
        logger.info('Email notification sent successfully')
    except Exception as e:
        logger.error(f'Failed to send email notification: {e}')
    return 'Task completed!'

@shared_task
def send_daily_notifications():
    today = timezone.now().date()
    
    # Get all recipes that received likes today
    liked_recipes = Recipe.objects.filter(recipelike__created__date=today).distinct()
    #liked_recipes = Recipe.objects.all()

    for recipe in liked_recipes:
        email = recipe.author.email
        recipe_id = recipe.id
        recipe_name = recipe.title
        subject = 'Recipe Like Notification'
        message = f'Your recipe "{recipe_name}" has received new likes today!'
        from_email = 'manoj.venkateshgowda@campusuvce.in'  
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            logger.info(f'Email notification sent successfully for recipe ID {recipe_id}')
        except Exception as e:
            logger.error(f'Failed to send email notification for recipe ID {recipe_id}: {e}')
    
    return f'All notifications sent!,{liked_recipes}'

