"""
Management command to populate categories with 3-level hierarchy.

Usage: python manage.py populate_categories
"""

from django.core.management.base import BaseCommand
from Project.models import Category
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populates categories with 3-level hierarchical structure (Main → Sub → Items)'

    def handle(self, *args, **kwargs):
        # User's specific Web Development structure (The Source of Truth for Web Dev)
        web_dev_categories = {
            "Core Development": {
                "description": "Fundamental web development services",
                "subcategories": {
                    "Frontend Development": {
                        "description": "Client-side web development",
                        "items": ["SPA Development (React, Vue, Angular)", "Responsive Web Design (HTML/CSS/JS)", "UI/UX Implementation", "Frontend Performance Optimization"]
                    },
                    "Backend Development": {
                        "description": "Server-side web development",
                        "items": ["API Development (REST/GraphQL)", "Database Modeling & Mgmt (SQL/NoSQL)", "Server Logic (Python, Node.js, PHP)", "Security & Auth Implementation"]
                    },
                    "Full-Stack Development": {
                        "description": "End-to-end web development",
                        "items": ["End-to-End Application Development", "System Architecture & Cloud Deployment"]
                    },
                }
            },
            "Specialized Platforms & Systems": {
                "description": "Platform-specific development services",
                "subcategories": {
                    "CMS Development": {
                        "description": "Content Management Systems",
                        "items": ["WordPress (Themes, Plugins)", "Shopify (Themes, Custom Apps)", "Drupal/Joomla Customization", "CMS Migration"]
                    },
                    "E-commerce Development": {
                        "description": "Online store development",
                        "items": ["Payment Gateway Integration", "WooCommerce/Magento", "Inventory/Order Systems"]
                    },
                    "Hybrid Mobile App Development": {
                        "description": "Cross-platform mobile development",
                        "items": ["React Native", "Flutter"]
                    },
                    "Data and Automation": {
                        "description": "Data extraction and automation",
                        "items": ["Web Scraping & Data Extraction", "Custom Automation Tools"]
                    },
                }
            },
            "Design, Maintenance, & Optimization": {
                "description": "Design and optimization services",
                "subcategories": {
                    "Web Design and UX/UI": {
                        "description": "User interface and experience",
                        "items": ["User Interface (UI) Design", "User Experience (UX) Research", "Prototyping and Testing"]
                    },
                    "Maintenance and Support": {
                        "description": "Ongoing website support",
                        "items": ["Bug Fixes & Debugging", "Security Patching & Monitoring", "Hosting/Server Management"]
                    },
                    "Technical Compliance": {
                        "description": "Technical standards and compliance",
                        "items": ["Technical SEO", "Web Accessibility (WCAG)"]
                    },
                }
            }
        }

        # Expanded General Freelancing Categories (3-Level Structure)
        general_categories = {
            "Graphics & Design": {
                "description": "Visual design and branding services",
                "subcategories": {
                    "Logo & Brand Identity": {
                        "description": "Brand visual elements",
                        "items": ["Logo Design", "Brand Style Guides", "Business Cards & Stationery"]
                    },
                    "Web & App Design": {
                        "description": "Digital interface design",
                        "items": ["Website Design", "App Design", "UX Design", "Landing Page Design", "Icon Design"]
                    },
                    "Art & Illustration": {
                        "description": "Creative artwork",
                        "items": ["Illustration", "NFT Art", "Pattern Design", "Portraits & Caricatures", "Cartoons & Comics"]
                    },
                    "Marketing Design": {
                        "description": "Design for marketing materials",
                        "items": ["Social Media Design", "Email Design", "Web Banners", "Brochure Design"]
                    }
                }
            },
            "Digital Marketing": {
                "description": "Online marketing services",
                "subcategories": {
                    "Search Optimization (SEO)": {
                        "description": "Improve search rankings",
                        "items": ["On-Page SEO", "Off-Page SEO", "Technical SEO", "Keyword Research"]
                    },
                    "Social Media": {
                        "description": "Social media management",
                        "items": ["Social Media Management", "Paid Social Media", "Influencer Marketing", "Community Management"]
                    },
                    "Advertising": {
                        "description": "Paid advertising campaigns",
                        "items": ["Google Ads (PPC)", "Facebook Ads", "Display Advertising", "Video Marketing"]
                    },
                    "Content Marketing": {
                        "description": "Content strategy and creation",
                        "items": ["Content Strategy", "Guest Posting", "Email Marketing", "Text Message Marketing"]
                    }
                }
            },
            "Writing & Translation": {
                "description": "Text and translation services",
                "subcategories": {
                    "Content Writing": {
                        "description": "Web and article writing",
                        "items": ["Articles & Blog Posts", "Website Content", "Product Descriptions", "Case Studies"]
                    },
                    "Copywriting": {
                        "description": "Sales and marketing copy",
                        "items": ["Sales Copy", "Ad Copy", "Email Copy", "Social Media Copy", "Landing Page Copy"]
                    },
                    "Technical & Business": {
                        "description": "Professional documentation",
                        "items": ["Technical Writing", "Business Plans", "White Papers", "Grant Writing", "Resumes & Cover Letters"]
                    },
                    "Translation": {
                        "description": "Language services",
                        "items": ["Translation", "Localization", "Transcription", "Proofreading & Editing"]
                    }
                }
            },
            "Video & Animation": {
                "description": "Video production services",
                "subcategories": {
                    "Video Editing": {
                        "description": "Post-production",
                        "items": ["Video Editing", "Visual Effects", "Color Grading", "Subtitles & Captions"]
                    },
                    "Animation": {
                        "description": "Animated content",
                        "items": ["2D Animation", "3D Animation", "Motion Graphics", "Whiteboard Animation", "Character Animation"]
                    },
                    "Social & Marketing Video": {
                        "description": "Video for social media",
                        "items": ["Video Ads & Commercials", "Social Media Videos", "Explainer Videos", "Corporate Videos"]
                    }
                }
            },
            "Music & Audio": {
                "description": "Audio production services",
                "subcategories": {
                    "Production & Composition": {
                        "description": "Music creation",
                        "items": ["Producers & Composers", "Beat Making", "Songwriters", "Jingles & Intros"]
                    },
                    "Voice & Narration": {
                        "description": "Vocal services",
                        "items": ["Voice Over", "Singers & Vocalists", "Audiobook Production"]
                    },
                    "Mixing & Mastering": {
                        "description": "Audio engineering",
                        "items": ["Mixing", "Mastering", "Audio Editing", "Vocal Tuning"]
                    }
                }
            },
            "Programming & Tech (General)": {
                "description": "General technical services",
                "subcategories": {
                    "Mobile Apps": {
                        "description": "Mobile application development",
                        "items": ["Android App Development", "iOS App Development", "Cross-Platform Apps", "Mobile Game Development"]
                    },
                    "Desktop Applications": {
                        "description": "Desktop software",
                        "items": ["Desktop Software Development", "Support & IT"]
                    },
                    "Data Science": {
                        "description": "Data analysis and AI",
                        "items": ["Data Analysis & Visualization", "Machine Learning", "AI Services", "Data Engineering"]
                    },
                    "Cybersecurity": {
                        "description": "Security services",
                        "items": ["Penetration Testing", "Security Audits", "Malware Removal"]
                    }
                }
            },
            "Business": {
                "description": "Business support services",
                "subcategories": {
                    "Virtual Assistant": {
                        "description": "Administrative support",
                        "items": ["Virtual Assistant", "Data Entry", "Market Research", "Project Management"]
                    },
                    "Legal & Financial": {
                        "description": "Professional consulting",
                        "items": ["Legal Consulting", "Financial Consulting", "Business Consulting", "HR Consulting"]
                    }
                }
            }
        }

        # Merge dictionaries
        all_categories = {**web_dev_categories, **general_categories}

        self.stdout.write(self.style.SUCCESS('Starting comprehensive 3-level category population...'))
        
        created_count = 0
        updated_count = 0

        for main_name, main_data in all_categories.items():
            # Create or update Main Category
            main_category, created = Category.objects.get_or_create(
                name=main_name,
                defaults={
                    'slug': slugify(main_name),
                    'description': main_data['description'],
                    'parent': None
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created Main: {main_name}'))
            else:
                main_category.description = main_data['description']
                main_category.save()
                updated_count += 1
                self.stdout.write(f'  Updated Main: {main_name}')

            # Create or update Subcategories
            for sub_name, sub_data in main_data['subcategories'].items():
                subcategory, created = Category.objects.get_or_create(
                    name=sub_name,
                    defaults={
                        'slug': slugify(sub_name),
                        'description': sub_data['description'],
                        'parent': main_category,
                        'items': sub_data['items']
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created Sub: {sub_name} ({len(sub_data["items"])} items)'))
                else:
                    subcategory.items = sub_data['items']
                    subcategory.description = sub_data['description']
                    subcategory.parent = main_category # Ensure parent is correct
                    subcategory.save()
                    updated_count += 1
                    self.stdout.write(f'    Updated Sub: {sub_name} ({len(sub_data["items"])} items)')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Done! Created {created_count}, Updated {updated_count} categories.'))
