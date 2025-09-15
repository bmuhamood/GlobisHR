from django.db import models

# About Us
class AboutUs(models.Model):
    title = models.CharField(max_length=255, default="About Our Company")
    description = models.TextField()

    companies_served = models.PositiveIntegerField(default=0)
    successful_placements = models.PositiveIntegerField(default=0)
    countries_covered = models.PositiveIntegerField(default=0)
    client_satisfaction = models.PositiveIntegerField(default=0, help_text="Enter percentage (0–100)")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Services
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome/Bootstrap icon class")

    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
    ]

    WORK_SCOPE_CHOICES = [
        ('inside_country', 'Inside Country'),
        ('outside_country', 'Outside Country'),
        ('remote', 'Remote'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # New fields
    work_scope = models.CharField(max_length=20, choices=WORK_SCOPE_CHOICES, default='inside_country')
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cv = models.FileField(upload_to="cvs/")
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255, default="Admin")
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional media
    main_image = models.ImageField(upload_to='blog/main_images/', blank=True, null=True)
    
    def __str__(self):
        return self.title

# Optional: separate model for multiple images
class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog/images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

# Optional: separate model for multiple videos
class BlogVideo(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField(blank=True, null=True)  # e.g., YouTube link or video hosting link
    caption = models.CharField(max_length=255, blank=True, null=True)
    
# Offices
class Office(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    working_hours = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    google_map_link = models.URLField()

    def __str__(self):
        return f"{self.city}, {self.country}"


# Contact Inquiries
class ContactInquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name}"
