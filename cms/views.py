from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import (
    AboutUs, Service, Job, Application, 
    BlogPost, Office, ContactInquiry
)

def home(request):
    """Main homepage view"""
    # Get content from database
    about = AboutUs.objects.first()
    services = Service.objects.all()
    featured_jobs = Job.objects.filter(is_active=True).order_by('-posted_at')[:3]
    all_jobs = Job.objects.filter(is_active=True).order_by('-posted_at')
    blog_posts = BlogPost.objects.all().order_by('-created_at')[:3]
    offices = Office.objects.all().order_by('country')
    
    # Prepare office data for JavaScript
    offices_data = {}
    for office in offices:
        # Create a key based on country name (lowercase, no spaces)
        key = office.country.lower().replace(' ', '').replace('unitedstates', 'usa').replace('unitedkingdom', 'uk')
        
        offices_data[key] = {
            'label': f"{office.country} - {office.city}",
            'addressLines': office.address.split('\n') if office.address else [office.address],
            'hours': office.working_hours,
            'phone': office.phone,
            'email': office.email,
            'mapEmbed': office.google_map_link if office.google_map_link.startswith('http') else f"https://www.google.com/maps?q={office.address}&output=embed"
        }
    
    context = {
        'about': about,
        'services': services,
        'featured_jobs': featured_jobs,
        'all_jobs': all_jobs,
        'blog_posts': blog_posts,
        'offices': offices,
        'offices_json': json.dumps(offices_data),
    }
    
    return render(request, 'cms/index.html', context)

def jobs_list(request):
    """Job listings page with search and filter"""
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    
    jobs = Job.objects.filter(is_active=True)
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    jobs = jobs.order_by('-posted_at')
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique locations for filter
    all_locations = Job.objects.filter(is_active=True).values_list('location', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'location': location,
        'all_locations': all_locations,
    }
    
    return render(request, 'cms/partials/jobs_list.html', context)

def job_detail(request, job_id):
    """Individual job detail page"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    context = {
        'job': job,
    }
    return render(request, 'cms/job_detail.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'cms/job_detail.html', {'job': job})

@require_POST
def apply_job(request):
    """Handle job application submission via AJAX"""
    try:
        job_id = request.POST.get('job_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cv = request.FILES.get('cv')
        cover_letter = request.POST.get('cover_letter', '')
        
        # Validation
        if not all([job_id, name, email, phone, cv]):
            return JsonResponse({
                'success': False, 
                'message': 'All required fields must be filled.'
            })
        
        job = get_object_or_404(Job, id=job_id, is_active=True)
        
        # Create application
        application = Application.objects.create(
            job=job,
            name=name,
            email=email,
            phone=phone,
            cv=cv,
            cover_letter=cover_letter
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Application submitted successfully for {job.title}!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while submitting your application.'
        })

@require_POST  
def contact_inquiry(request):
    """Handle contact form submission via AJAX"""
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        # Validation
        if not all([name, email, message]):
            return JsonResponse({
                'success': False,
                'message': 'Name, email, and message are required.'
            })
        
        # Create contact inquiry
        inquiry = ContactInquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your inquiry! We will get back to you soon.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while sending your message.'
        })

def blog_list(request):
    """Blog posts listing page"""
    posts = BlogPost.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'cms/blog_list.html', context)

def blog_detail(request, post_id):
    """Individual blog post detail page"""
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Get related posts (same author or recent posts)
    related_posts = BlogPost.objects.exclude(id=post.id).order_by('-created_at')[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    
    return render(request, 'cms/blog_detail.html', context)

def services_detail(request):
    """Services page"""
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'cms/services_detail.html', context)

def about_detail(request):
    """About us page"""
    about = AboutUs.objects.first()
    context = {
        'about': about,
    }
    return render(request, 'cms/about_detail.html', context)

def contact_detail(request):
    """Contact page"""
    offices = Office.objects.all().order_by('country')
    
    # Prepare office data for JavaScript
    offices_data = {}
    for office in offices:
        key = office.country.lower().replace(' ', '').replace('unitedstates', 'usa').replace('unitedkingdom', 'uk')
        
        offices_data[key] = {
            'label': f"{office.country} - {office.city}",
            'addressLines': office.address.split('\n') if office.address else [office.address],
            'hours': office.working_hours,
            'phone': office.phone,
            'email': office.email,
            'mapEmbed': office.google_map_link if office.google_map_link.startswith('http') else f"https://www.google.com/maps?q={office.address}&output=embed"
        }
    
    context = {
        'offices': offices,
        'offices_json': json.dumps(offices_data),
    }
    
    return render(request, 'cms/contact_detail.html', context)

# API Views for AJAX calls
def get_jobs_ajax(request):
    """Get jobs list for AJAX filtering"""
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('type', '')
    
    jobs = Job.objects.filter(is_active=True)
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    # Note: You might want to add a job_type field to your Job model
    # if job_type:
    #     jobs = jobs.filter(job_type__icontains=job_type)
    
    jobs_data = []
    for job in jobs[:20]:  # Limit to 20 results
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'description': job.description[:100] + '...' if len(job.description) > 100 else job.description,
            'location': job.location,
            'posted_at': job.posted_at.strftime('%b %d, %Y'),
        })
    
    return JsonResponse({
        'success': True,
        'jobs': jobs_data
    })

def get_office_details(request, office_key):
    """Get specific office details for AJAX"""
    try:
        # Map office keys to country names
        key_mapping = {
            'usa': 'United States',
            'uk': 'United Kingdom', 
            'canada': 'Canada',
            'australia': 'Australia'
        }
        
        country_name = key_mapping.get(office_key.lower())
        if not country_name:
            return JsonResponse({'success': False, 'message': 'Office not found'})
        
        office = Office.objects.filter(country=country_name).first()
        if not office:
            return JsonResponse({'success': False, 'message': 'Office not found'})
        
        office_data = {
            'label': f"{office.country} - {office.city}",
            'addressLines': office.address.split('\n') if office.address else [office.address],
            'hours': office.working_hours,
            'phone': office.phone,
            'email': office.email,
            'mapEmbed': office.google_map_link if office.google_map_link.startswith('http') else f"https://www.google.com/maps?q={office.address}&output=embed"
        }
        
        return JsonResponse({
            'success': True,
            'office': office_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error retrieving office details'
        })