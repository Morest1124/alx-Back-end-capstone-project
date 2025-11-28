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
        # User's detailed Web Development structure
        web_dev_categories = {
            "Core Development": {
                "description": "Fundamental web development services",
                "subcategories": {
                    "Frontend Development": {
                        "description": "Client-side web development",
                        "items": [
                            "SPA Development (React, Vue, Angular)",
                            "Responsive Web Design (HTML/CSS/JS)",
                            "UI/UX Implementation",
                            "Frontend Performance Optimization"
                        ]
                    },
                    "Backend Development": {
                        "description": "Server-side web development",
                        "items": [
                            "API Development (REST/GraphQL)",
                            "Database Modeling & Mgmt (SQL/NoSQL)",
                            "Server Logic (Python, Node.js, PHP)",
                            "Security & Auth Implementation"
                        ]
                    },
                    "Full-Stack Development": {
                        "description": "End-to-end web development",
                        "items": [
                            "End-to-End Application Development",
                            "System Architecture & Cloud Deployment"
                        ]
                    },
                }
            },
            "Specialized Platforms & Systems": {
                "description": "Platform-specific development services",
                "subcategories": {
                    "CMS Development": {
                        "description": "Content Management Systems",
                        "items": [
                            "WordPress (Themes, Plugins)",
                            "Shopify (Themes, Custom Apps)",
                            "Drupal/Joomla Customization",
                            "CMS Migration"
                        ]
                    },
                    "E-commerce Development": {
                        "description": "Online store development",
                        "items": [
                            "Payment Gateway Integration",
                            "WooCommerce/Magento",
                            "Inventory/Order Systems"
                        ]
                    },
                    "Hybrid Mobile App Development": {
                        "description": "Cross-platform mobile development",
                        "items": [
                            "React Native",
                            "Flutter"
                        ]
                    },
                    "Data and Automation": {
                        "description": "Data extraction and automation",
                        "items": [
                            "Web Scraping & Data Extraction",
                            "Custom Automation Tools"
                        ]
                    },
                }
            },
            "Design, Maintenance, & Optimization": {
                "description": "Design and optimization services",
                "subcategories": {
                    "Web Design and UX/UI": {
                        "description": "User interface and experience",
                        "items": [
                            "User Interface (UI) Design",
                            "User Experience (UX) Research",
                            "Prototyping and Testing"
                        ]
                    },
                    "Maintenance and Support": {
                        "description": "Ongoing website support",
                        "items": [
                            "Bug Fixes & Debugging",
                            "Security Patching & Monitoring",
                            "Hosting/Server Management"
                        ]
                    },
                    "Technical Compliance": {
                        "description": "Technical standards and compliance",
                        "items": [
                            "Technical SEO",
                            "Web Accessibility (WCAG)"
                        ]
                    },
                }
            }
        }

        # General categories (existing structure kept simple)
        general_categories = {
            'Mobile Development': [
                'Android Development',
                'iOS Development',
                'React Native',
                'Flutter Development',
                'Mobile App Design',
            ],
            'Design & Creative': [
                'Logo Design',
                'UI/UX Design',
                'Graphic Design',
                'Illustration',
                'Brand Identity',
                '3D Design',
            ],
            'Writing & Translation': [
                'Content Writing',
                'Copywriting',
                'Technical Writing',
                'Translation',
                'Proofreading & Editing',
            ],
            'Digital Marketing': [
                'SEO',
                'Social Media Marketing',
                'Email Marketing',
                'Content Marketing',
                'PPC Advertising',
            ],
            'Video & Animation': [
                'Video Editing',
                'Animation',
                'Motion Graphics',
                'Whiteboard Animation',
                'Video Production',
            ],
            'Data Science & Analytics': [
                'Data Analysis',
                'Machine Learning',
                'Data Visualization',
                'Statistical Analysis',
                'Business Intelligence',
            ],
            'Programming & Tech': [
                'Python Development',
                'Java Development',
                'C++ Development',
                'DevOps',
                'Database Administration',
            ],
        }

        self.stdout.write(self.style.SUCCESS('Starting 3-level category population...'))
        
        created_count = 0
        updated_count = 0

        # Populate Web Development categories with 3-level structure
        for main_name, main_data in web_dev_categories.items():
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
                self.stdout.write(self.style.SUCCESS(f'✓ Created main category: {main_name}'))
            else:
                # Update description if exists
                main_category.description = main_data['description']
                main_category.save()
                updated_count += 1
                self.stdout.write(f'  Updated: {main_name}')

            # Create subcategories with items
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
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created subcategory: {sub_name} with {len(sub_data["items"])} items'))
                else:
                    # Update items if exists
                    subcategory.items = sub_data['items']
                    subcategory.description = sub_data['description']
                    subcategory.save()
                    updated_count += 1
                    self.stdout.write(f'    Updated: {sub_name} with {len(sub_data["items"])} items')

        # Populate general categories (simple 2-level structure)
        for main_category_name, subcategories in general_categories.items():
            main_category, created = Category.objects.get_or_create(
                name=main_category_name,
                defaults={
                    'slug': slugify(main_category_name),
                    'description': f'Professional services in {main_category_name}',
                    'parent': None
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created main category: {main_category_name}'))
            else:
                updated_count += 1
                self.stdout.write(f'  Exists: {main_category_name}')

            for subcategory_name in subcategories:
                subcategory, created = Category.objects.get_or_create(
                    name=subcategory_name,
                    defaults={
                        'slug': slugify(subcategory_name),
                        'description': f'{subcategory_name} services',
                        'parent': main_category,
                        'items': []  # No items for general categories
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n✅ Done! Created {created_count}, Updated {updated_count} categories.'))
