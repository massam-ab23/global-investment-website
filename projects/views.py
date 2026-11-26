from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ProjectForm  # Ensure this line is included
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from .forms import CollaboratorInviteForm
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import pprint
from django.template.loader import render_to_string
import os  # Add this line
from django.contrib.auth import get_user_model
from .models import Project, Activity, Notification
from .forms import ProjectForm, ApplyToInvestForm  # ✅ CORRECT
from .forms import InvestmentApplicationForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Project  # Assuming sectors are part of the Project model
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserProfileForm
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.utils.translation import activate, gettext as _, get_language
from django.utils.html import strip_tags
from django.templatetags.static import static
from django.shortcuts import render, get_object_or_404
from datetime import datetime
import calendar
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView
from .forms import ContactForm
from django.views.decorators.csrf import csrf_exempt
import json


def landing_page(request):
    # Debugging the current session language
    session_lang = request.session.get('django_language', 'Not Set')
    print("Session Language Before Activate:", session_lang)

    if request.method == 'POST' and 'language' in request.POST:
        language_code = request.POST['language']
        activate(language_code)
        request.session['django_language'] = language_code
        print("Active Language After Activate:", get_language())

    # Confirm the language is being stored
    print("Current Language in Session:", request.session.get('django_language', 'Not Set'))

    search_query = request.GET.get('search', '')
    sector_filter = request.GET.get('sector', '')
    country_filter = request.GET.get('country', '')

    # ✅ Handle notifications safely
    unread_notifications_count = 0  # Default for anonymous users
    unread_notifications = []

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notifications_count = unread_notifications.count()

    # Fetch all projects
    projects = Project.objects.all()

    # Apply filters
    if search_query:
        projects = projects.filter(title__icontains=search_query)
    if sector_filter:
        projects = projects.filter(sector=sector_filter)
    if country_filter:
        projects = projects.filter(country__icontains=country_filter)

    # Separate the first 0 featured projects
    featured_projects = list(projects[:0])  # Convert to a list

    # Exclude the first 0 projects from the remaining ones
    #remaining_projects = projects[0:]

    # Decide on pagination: 6 images per page or 4 images per page
    #images_per_page = 6  # Change to 4 if you want 4 images per page

    # Paginate only the remaining projects
    #paginator = Paginator(remaining_projects, images_per_page)
    #page_number = request.GET.get('page', 1)
    #paginated_projects = paginator.get_page(page_number)
    # ✅ Limit to first 6 projects only
    remaining_projects = projects[:6]  # This will ensure only 6 sectors are shown

# ✅ No pagination needed (remove paginator)


    # Debugging outputs
    #print("Page Number:", page_number)
    print("Featured Projects Count:", len(featured_projects))
    print("Remaining Projects Count:", remaining_projects.count())
    #print("Projects on Current Page:", len(paginated_projects.object_list))

    context = {
        # ✅ Include notifications, safely handling anonymous users
        'unread_notifications': unread_notifications if request.user.is_authenticated else [],
        'unread_notifications_count': unread_notifications_count,
        'SECTOR_CHOICES': Project.SECTOR_CHOICES,
        'featured_projects': featured_projects,  # Display only on the home page
        #'remaining_projects': paginated_projects,  # Paginated sectors
        #'page_obj': paginated_projects,  # Add this line to pass the paginator object as 'page_obj'
        'remaining_projects': remaining_projects,  # Only show first 6 sectors

    }
    return render(request, 'landing.html', context)

# Project Detail View with Collaborators
#@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    collaborators = project.collaborators.all()
    invite_form = CollaboratorInviteForm()

    # Determine the image URL for the project's sector
    sector_image_filename = f"{project.sector.lower().replace(' ', '-')}.jpg" if project.sector else "placeholder.jpg"
    image_path = os.path.join(settings.STATICFILES_DIRS[0], "images", sector_image_filename)

    if os.path.exists(image_path):
        image_url = f"{settings.STATIC_URL}images/{sector_image_filename}"
    else:
        image_url = f"{settings.STATIC_URL}images/placeholder.jpg"  # Fallback image

    if request.method == 'POST':
        invite_form = CollaboratorInviteForm(request.POST)
        if invite_form.is_valid():
            collaborator = invite_form.cleaned_data['email_or_username']
            if collaborator not in collaborators:
                project.collaborators.add(collaborator)

                # Create a notification for the invited user
                Notification.objects.create(
                    user=collaborator,
                    message=f"You have been added as a collaborator to the project: {project.title}",
                    is_read=False
                )

                # Send email notification
                subject = f"You've been added as a collaborator on {project.title}"
                message = render_to_string('emails/collaborator_invite.html', {
                    'project': project,
                    'collaborator': collaborator,
                    'owner': project.owner,
                })

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [collaborator.email],
                    fail_silently=False,
                )

                # Add a success message for the user adding the collaborator
                messages.success(request, f"{collaborator.get_full_name() or collaborator.username} has been added as a collaborator!")
            else:
                messages.warning(request, "This user is already a collaborator.")
            return redirect('project_detail', pk=pk)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'collaborators': collaborators,
        'invite_form': invite_form,
        'image_url': image_url,  # Pass the image URL to the template
    })

 
# About Eritrea View
def about_page(request):
    return render(request, 'about.html')


@staff_member_required
def create_project(request):
    """Handles project creation (NOT investment applications)."""
    print("🚨 DEBUG: create_project() function called 🚨")  # ✅ Add Debugging Here

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            # ✅ Notification for a NEW project
            Notification.objects.create(
                user=request.user,
                message=f"{request.user.get_full_name()} created a new project: {project.title}.",
                is_read=False
            )

            # ✅ Email notification
            send_mail(
                subject="New Project Created",
                message=f"A new project has been created by {project.owner.get_full_name()}.\n"
                        f"Sector: {project.sector}\n"
                        f"Description: {project.description}\n"
                        f"Contact Information: {project.contact_information}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Your project has been created successfully.")
            return redirect('landing')
    else:
        form = ProjectForm()

    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def apply_to_invest(request, project_id):
    # Check if project_id is 0 or a valid ID
    if project_id == 0:
        # For a general "Apply to Invest" form, no specific project
        if request.method == 'POST':
            form = ApplyToInvestForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.user = request.user
                application.title = "General Investment Application"
                application.save()

                # General Notification
                Notification.objects.create(
                    user=request.user,
                    message="You have successfully submitted a general investment application.",
                    is_read=False,
                )

                # General Email to Admin
                send_mail(
                    'General Investment Application',
                    f'{request.user.get_full_name()} has submitted a general investment application.',
                    settings.EMAIL_HOST_USER,
                    ['mollieabrham@gmail.com'],  # Replace with admin's email
                    fail_silently=False,
                )

                messages.success(request, "Your general application has been submitted successfully.")
                return redirect('investment_success')
            else:
                messages.error(request, "Please correct the errors in the form.")
        else:
            form = ApplyToInvestForm()

        return render(request, 'projects/apply_to_invest.html', {'form': form, 'project': None})

    # Handle specific project application
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        messages.error(request, "The project you're trying to apply for does not exist.")
        return redirect('landing')

    if request.method == 'POST':
        form = ApplyToInvestForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.title = project.title
            application.sector = project.sector
            application.country = project.country
            application.save()

            # Send notifications and emails
            Notification.objects.create(
                user=request.user,
                message=f"You have successfully applied to invest in {project.title}.",
                is_read=False,
            )
            Notification.objects.create(
                user=project.owner,
                message=f"{request.user.get_full_name()} has applied to invest in your project: {project.title}.",
                is_read=False,
            )

            send_mail(
                'New Investment Application',
                f'{request.user.get_full_name()} has applied to invest in {project.title}.',
                settings.EMAIL_HOST_USER,
                ['admin@example.com'],  # Replace with admin's email
                fail_silently=False,
            )

            messages.success(request, "Your application has been submitted successfully.")
            return redirect('investment_success')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ApplyToInvestForm()

    return render(request, 'projects/apply_to_invest.html', {'form': form, 'project': project})



@login_required
def investment_success(request):
    return render(request, 'projects/investment_success.html')


@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    
    # Only the owner of the notification can delete it
    if request.method == 'POST':
        notification.delete()
        messages.success(request, "Notification deleted successfully.")
        return redirect('notifications')  # Replace with the name of your notifications view
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@staff_member_required
def edit_project(request, pk):
    """Handles project editing (restricted to admins)."""
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your project has been updated successfully!')
            return redirect('my_projects')  # Redirect to "My Projects"
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})



@login_required
def my_projects(request):
    user_projects = Project.objects.filter(owner=request.user)
    total_investment = user_projects.aggregate(models.Sum('investment_required'))['investment_required__sum'] or 0
    total_collaborators = sum(project.collaborators.count() for project in user_projects)

    context = {
        'user_projects': user_projects,
        'total_projects': user_projects.count(),
        'total_investment': total_investment,
        'total_collaborators': total_collaborators,
    }
    
    # Get search and filter parameters from the request
    search_query = request.GET.get('search', '')
    sector_filter = request.GET.get('sector', '')
    status_filter = request.GET.get('status', '')

    # Fetch projects created by the logged-in user
    user_projects = Project.objects.filter(owner=request.user)

    # Apply filters
    if search_query:
        user_projects = user_projects.filter(title__icontains=search_query)
    if sector_filter:
        user_projects = user_projects.filter(sector=sector_filter)
    if status_filter:
        user_projects = user_projects.filter(status=status_filter)

    # Set up pagination
    paginator = Paginator(user_projects, 5)  # Display 5 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get sector and status choices for the filter dropdowns
    sectors = Project.SECTOR_CHOICES
    statuses = Project._meta.get_field('status').choices

    context = {
        'page_obj': page_obj,  # Pass paginated projects
        'sectors': sectors,
        'statuses': statuses,
        'search_query': search_query,
        'sector_filter': sector_filter,
        'status_filter': status_filter,
    }
    return render(request, 'projects/my_projects.html', context)

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your project has been updated successfully!')
            return redirect('my_projects')  # Redirect to "My Projects"
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Your project has been deleted successfully!')
        return redirect('my_projects')
    return render(request, 'projects/delete_project.html', {'project': project})

@login_required
def remove_collaborator(request, project_id, collaborator_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        User = get_user_model()
        collaborator = get_object_or_404(User, id=collaborator_id)

        # Check permission
        if request.user != project.owner:
            return JsonResponse({"error": "Permission denied"}, status=403)

        # Remove collaborator
        project.collaborators.remove(collaborator)

        # Remove notifications related to this collaborator
        Notification.objects.filter(
            user=request.user,
            message__icontains=f"{collaborator.username}"
        ).delete()

        return JsonResponse({"success": "Collaborator removed successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=400)
    
# Email Notification Function
def send_email_notification(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )

# Notifications View
@login_required
def notifications_view(request):
    # Fetch user's notifications
    notifications = request.user.notifications.all()

    # Mark all unread notifications as read
    notifications.filter(is_read=False).update(is_read=True)

    # Render the notifications page
    return render(request, 'projects/notifications.html', {'notifications': notifications})



@login_required
def mark_notifications_as_read(request):
    if request.method == 'POST':
        # Mark all unread notifications for the user as read
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return redirect('notifications')  # Redirect to the notifications page
    return JsonResponse({'success': False}, status=400)


# Define the admin username (you can also check for superuser)
ADMIN_USERNAME = "M.Abraham"  # Change this to your actual username

@login_required
def profile(request):
    """ ✅ Display user profile (or create if missing) """
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'user': request.user, 'profile': user_profile})


@login_required
def edit_profile(request, user_id=None):
    """
    ✅ Admins can edit any profile.
    ✅ Users can only edit their own profile.
    ❌ Users CANNOT edit the admin's profile.
    """

    # 🔹 Determine which profile is being edited
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)  # Get user by ID
        user_profile, created = UserProfile.objects.get_or_create(user=profile_user)
    else:
        profile_user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # ❌ Prevent users from editing the admin’s profile
    if profile_user.username.lower() == ADMIN_USERNAME.lower() and request.user != profile_user:
        messages.error(request, "You do not have permission to edit the admin's profile.")
        return redirect('profile')

    # ❌ Regular users can only edit their own profile
    if request.user != profile_user and not request.user.is_superuser:
        messages.error(request, "You can only edit your own profile.")
        return redirect('profile')

    # ✅ Allow profile updates
    if request.method == 'POST':
        print("POST Data:", request.POST)  # ✅ Debugging: Print form data
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            print("Saved Country:", user_profile.country)  # ✅ Debugging: Check after saving
            messages.success(request, "Profile updated successfully!")
            return redirect('profile', user_id=profile_user.id if request.user.is_superuser else None)
        else:
            print("Form Errors:", form.errors)  # ✅ Debugging: Print form errors
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/edit_profile.html', {'form': form, 'profile_user': profile_user})

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            subject = f"Contact Us Inquiry from {name} {last_name}"
            email_message = f"Name: {name} {last_name}\nEmail: {email}\n\nMessage:\n{message}"
            recipient_list = [settings.CONTACT_EMAIL]  # Replace with your admin email

            try:
                send_mail(subject, email_message, email, recipient_list)
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                messages.error(request, "There was an error sending your message. Please try again later.")
        else:
            messages.error(request, "Invalid reCAPTCHA. Please verify you're human.")

    else:
        form = ContactForm()

    return render(request, "projects/contact_us.html", {"form": form})

def some_view(request):
    translated_text = _("This text will be translated.")
    return render(request, "template.html", {"translated_text": translated_text})


def language_selection(request):
    current_language_code = get_language()
    current_language_name = dict(settings.LANGUAGES).get(current_language_code, "Language")
    return render(request, 'language_selection.html', {
        'languages': settings.LANGUAGES,
        'current_language_name': current_language_name,
    })


def multisector_view(request):
    projects = Project.objects.all()  # Fetch all projects/sectors
    return render(request, "projects/multisector.html", {"projects": projects})

def history_view(request):
    return render(request, "projects/history.html")  # ✅ Make sure this template exists

def music_view(request):
    return render(request, "projects/music.html")  # ✅ Make sure this template exists

def send_donation_receipt(donor_email, donor_name, amount, transaction_id):
    """Send a thank-you email & receipt to the donor."""
    
    subject = "Thank You for Your Donation!"

    # Render the email template
    html_message = render_to_string('emails/donation_receipt.html', {
        'donor_name': donor_name,
        'amount': amount,
        'transaction_id': transaction_id
    })

    plain_message = strip_tags(html_message)  # Convert to plain text

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [donor_email],
        html_message=html_message,
        fail_silently=False,
    )


def paypal_payment_success(request):
    """Handle successful PayPal donation."""
    if request.method == "POST":
        donor_email = request.POST.get("payer_email")
        donor_name = request.POST.get("payer_name")
        amount = request.POST.get("amount")
        transaction_id = request.POST.get("txn_id")

        # Send thank-you email
        send_donation_receipt(donor_email, donor_name, amount, transaction_id)

        messages.success(request, "Thank you for your donation! A receipt has been sent to your email.")
        return redirect("thank_you_page")

    return redirect("home")

@csrf_exempt
def paypal_webhook(request):
    """ Handle PayPal IPN/Webhooks """
    try:
        payload = json.loads(request.body)

        if payload["event_type"] == "PAYMENT.SALE.COMPLETED":
            donor_email = payload["resource"]["payer"]["email_address"]
            donor_name = payload["resource"]["payer"]["name"]["given_name"]
            donor_last_name = payload["resource"]["payer"]["name"]["surname"]
            amount = payload["resource"]["amount"]["total"]
            currency = payload["resource"]["amount"]["currency_code"]

            # Send email to donor
            subject = "Thank You for Your Donation!"
            message = f"Dear {donor_name} {donor_last_name},\n\n"
            message += f"Thank you for your generous donation of {amount} {currency}.\n"
            message += "Your support helps us continue our mission!\n\nBest regards,\n Eritrean Investment Community."

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Your sender email (configure in settings.py)
                [donor_email],
                fail_silently=False,
            )

            # Notify admin
            admin_message = f"New donation received from {donor_name} {donor_last_name}\n"
            admin_message += f"Amount: {amount} {currency}\nEmail: {donor_email}"

            send_mail(
                "New PayPal Donation Received",
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Change to your admin email
                fail_silently=False,
            )

        return JsonResponse({"status": "success"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def search_results(request):
    query = request.GET.get('q')
    results = Project.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)) if query else Project.objects.none()
    return render(request, 'projects/search_results.html', {'results': results, 'query': query})

def calendar_view(request):
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day

    # Generate structured calendar data
    calendar_data = {}
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        month_days = calendar.monthcalendar(current_year, month)  # List of weeks
        calendar_data[month_name] = month_days

    return render(request, 'projects/calendar.html', {
        'current_year': current_year,
        'current_month': current_month,
        'current_day': current_day,
        'calendar_data': calendar_data
    })

    
def news_view(request):
    return render(request, 'projects/news.html')

# Full sector data (with images & descriptions) for the Multisector dropdown.
SECTOR_DATA = {
    "Agriculture": {
        "image": "images/agriculture.jpg",
        "description": "Agriculture is vital to Eritrea's economy, offering sustainable farming opportunities."
    },
    "Energy": {
        "image": "images/energy.jpg",
        "description": "The energy sector focuses on renewable solutions, including solar and wind power."
    },
    "Mining": {
        "image": "images/mining.jpg",
        "description": "Eritrea has rich mineral resources, including gold, copper, and potash."
    },
    "Education": {
        "image": "images/education.jpg",
        "description": "Investment in education enhances workforce skills and long-term economic growth."
    },
    "Tourism": {
        "image": "images/tourism.jpg",
        "description": "Eritrea’s coastline and historical sites offer opportunities for tourism development."
    },
    "Irrigation": {
        "image": "images/irrigation.jpg",
        "description": "Irrigation projects improve water supply for agriculture and rural development."
    },
    "Technology": {
        "image": "images/technology.jpg",
        "description": "The tech industry is growing rapidly, with opportunities in software and innovation."
    },
    "Healthcare": {
        "image": "images/healthcare.jpg",
        "description": "The healthcare sector focuses on expanding access to medical services and pharmaceuticals."
    },
    "Finance": {
        "image": "images/finance.jpg",
        "description": "Eritrea’s financial sector is developing with opportunities in banking and investment."
    },
    "Robotics": {
        "image": "images/robotics.jpg",
        "description": "Robotics and automation are transforming industries, creating new investment areas."
    },
    "Artificial_Intelligence": {  # ✅ MATCH models.py
        "image": "images/artificial_intelligence.jpg",
        "description": "Artificial intelligence is a game changer in business automation and data processing."
    },
    "Manufacturing": {
        "image": "images/manufacturing.jpg",
        "description": "Manufacturing sector drives industrial growth and job creation in Eritrea."
    },
    "Retail": {
        "image": "images/retail.jpg",
        "description": "Retail industry in Eritrea is expanding, with new markets and business opportunities."
    },
    "Real_Estate": {  # ✅ FIXED TO MATCH models.py
        "image": "images/real_estate.jpg",
        "description": "Real estate investments are growing with demand for housing and commercial spaces."
    },
    "Transportation": {
        "image": "images/transportation.jpg",
        "description": "Transportation sector is crucial for economic connectivity and trade development."
    },
    "Logistics": {
        "image": "images/logistics.jpg",
        "description": "Logistics industry supports trade, distribution, and supply chain efficiency."
    },
    "Media": {
        "image": "images/media.jpg",
        "description": "Media industry is evolving with digital platforms and content creation."
    },
    "Entertainment": {
        "image": "images/entertainment.jpg",
        "description": "Entertainment sector includes film, music, and cultural activities."
    },
    "Sports": {
        "image": "images/sports.jpg",
        "description": "Investment in sports infrastructure and events promotes tourism and youth development."
    },
    "Aerospace": {
        "image": "images/aerospace.jpg",
        "description": "Aerospace sector offers opportunities in aviation technology and aircraft maintenance."
    },
    "Defense": {
        "image": "images/defense.jpg",
        "description": "Defense industry includes security systems, infrastructure, and strategic investments."
    },
    "Environment": {
        "image": "images/environment.jpg",
        "description": "Sustainable environmental solutions are essential for green energy and conservation."
    },
    "Water_Resources": {  # ✅ FIXED TO MATCH models.py
        "image": "images/water_resources.jpg",
        "description": "Water resource management is key to agricultural growth and clean water access."
    },
    "Food_Processing": {  # ✅ FIXED TO MATCH models.py
        "image": "images/food_processing.jpg",
        "description": "Food processing industry is growing with demand for packaged and processed foods."
    },
    "Pharmaceuticals": {
        "image": "images/pharmaceuticals.jpg",
        "description": "Pharmaceutical sector is advancing with investments in medicine production."
    },
    "Biotechnology": {
        "image": "images/biotechnology.jpg",
        "description": "Biotechnology innovation supports agriculture, healthcare, and medical research."
    },
    "Telecommunications": {
        "image": "images/telecommunications.jpg",
        "description": "Telecommunications sector is expanding with increased mobile and internet services."
    },
    "E_Commerce": {  # ✅ MATCH models.py
        "image": "images/e_commerce.jpg",
        "description": "E-Commerce is transforming retail with digital shopping and online businesses."
    },
    "Consulting": {
        "image": "images/consulting.jpg",
        "description": "Consulting services support businesses with expertise and strategic solutions."
    },
    "Fashion": {
        "image": "images/fashion.jpg",
        "description": "Fashion industry includes apparel, textile manufacturing, and retail markets."
    },
    "Automotive": {
        "image": "images/automotive.jpg",
        "description": "Automotive sector is growing with vehicle production and transportation investments."
    },
    "Non_Profit": {  # ✅ MATCH models.py
        "image": "images/non_profit.jpg",
        "description": "Non-Profit organizations focus on social impact, charity, and humanitarian aid."
    },
    "Public_Administration": {  # ✅ FIXED TO MATCH models.py
        "image": "images/public_administration.jpg",
        "description": "Public administration focuses on governance, policy making, and development projects."
    }
}

from django.utils.translation import gettext as _

def sector_detail(request, sector_name):
    print(f"📌 Incoming sector_name: {sector_name}")  # Debugging
    
    # Try exact match first
    sector = Project.objects.filter(sector=sector_name).first()

    if not sector:
        # Convert hyphens to spaces and try again
        sector_name_clean = sector_name.replace("-", " ")
        sector = Project.objects.filter(sector=sector_name_clean).first()
        print(f"🔄 Retrying with: {sector_name_clean}, Found: {bool(sector)}")

    if not sector:
        return render(request, "404.html", {"message": f"Sector '{sector_name}' not found"}, status=404)

    # Translate the sector name
    translated_sector_name = _(sector_name)  # ✅ Use gettext to translate

    image_filename = sector_name.lower().replace(" ", "-") + ".jpg"
    print(f"🖼️ Image file should be: {image_filename}")

    context = {
        "sector_name": sector.sector,  # Keep original for debugging
        "translated_sector_name": translated_sector_name,  # ✅ Now it's translated!
        "sector_image_url": f"/static/images/{image_filename}",
        "sector_description": sector.description,
        "investment_required": sector.investment_required,
        "status": sector.status,
        "created_at": sector.created_at,
        "updated_at": sector.updated_at
    }

    return render(request, "projects/sector_detail.html", context)


class HomeView(TemplateView):
    template_name = "home.html"  # ✅ Make sure this matches your actual template name

