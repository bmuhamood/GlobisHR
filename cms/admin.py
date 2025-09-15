from django.contrib import admin
from .models import (
    AboutUs, Service, Job, Application, 
    BlogPost, Office, ContactInquiry, BlogPost, BlogImage, BlogVideo
)

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'companies_served', 'successful_placements', 'countries_covered', 'client_satisfaction', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Statistics', {
            'fields': ('companies_served', 'successful_placements', 'countries_covered', 'client_satisfaction'),
            'description': 'These numbers will be displayed on the About section.'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one AboutUs instance
        return not AboutUs.objects.exists()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    list_editable = ('icon',)
    search_fields = ('name', 'description')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'icon'),
            'description': 'Icon should be a FontAwesome class like "fas fa-user-tie"'
        }),
    )

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'job_type', 'work_scope', 'posted_at', 'is_active', 'application_count')
    list_filter = ('is_active', 'posted_at', 'location', 'job_type', 'work_scope')
    list_editable = ('is_active',)
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('posted_at',)

    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'description', 'location', 'job_type', 'work_scope', 'salary_range')
        }),
        ('Status', {
            'fields': ('is_active', 'posted_at')
        }),
    )

    def application_count(self, obj):
        return obj.applications.count()
    application_count.short_description = 'Applications'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'job', 'email', 'phone', 'applied_at')
    list_filter = ('applied_at',)
    search_fields = ('name', 'email', 'phone', 'job__title')
    readonly_fields = ('applied_at',)

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1  # allow adding one image by default

class BlogVideoInline(admin.TabularInline):
    model = BlogVideo
    extra = 1  # allow adding one video by default

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    inlines = [BlogImageInline, BlogVideoInline]

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'phone', 'email')
    list_filter = ('country',)
    search_fields = ('country', 'city', 'address')
    
    fieldsets = (
        ('Location', {
            'fields': ('country', 'city', 'address')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'working_hours')
        }),
        ('Map', {
            'fields': ('google_map_link',),
            'description': 'Enter Google Maps embed URL or address for automatic map generation'
        }),
    )

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('submitted_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('message', 'submitted_at')
        }),
    )
    
    def has_add_permission(self, request):
        # Inquiries should only be created through the website
        return False

# Customize admin site
admin.site.site_header = "Globis HR Solutions Admin"
admin.site.site_title = "Globis HR Admin"
admin.site.index_title = "Welcome to Globis HR Solutions Administration"