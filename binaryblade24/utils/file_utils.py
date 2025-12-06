"""
File upload utilities for handling file validation, storage, and processing.
"""
import os
import hashlib
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError


# File type categories and allowed extensions
FILE_CATEGORIES = {
    'image': {
        'extensions': ['jpg', 'jpeg', 'png', 'webp', 'gif', 'svg', 'bmp'],
        'max_size': 5 * 1024 * 1024,  # 5MB
        'mime_types': ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml', 'image/bmp']
    },
    'video': {
        'extensions': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'],
        'max_size': 100 * 1024 * 1024,  # 100MB
        'mime_types': ['video/mp4', 'video/x-msvideo', 'video/quicktime', 'video/x-ms-wmv', 'video/x-flv', 'video/x-matroska', 'video/webm']
    },
    'document': {
        'extensions': ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt'],
        'max_size': 10 * 1024 * 1024,  # 10MB
        'mime_types': ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/rtf']
    },
    'spreadsheet': {
        'extensions': ['xls', 'xlsx', 'csv', 'ods'],
        'max_size': 10 * 1024 * 1024,  # 10MB
        'mime_types': ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv']
    },
    'presentation': {
        'extensions': ['ppt', 'pptx', 'odp'],
        'max_size': 15 * 1024 * 1024,  # 15MB
        'mime_types': ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']
    },
    'archive': {
        'extensions': ['zip', 'rar', '7z', 'tar', 'gz'],
        'max_size': 50 * 1024 * 1024,  # 50MB
        'mime_types': ['application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed', 'application/x-tar', 'application/gzip']
    },
    'code': {
        'extensions': ['py', 'js', 'jsx', 'ts', 'tsx', 'java', 'cpp', 'c', 'cs', 'php', 'rb', 'go', 'rs', 'swift', 'kt', 'html', 'css', 'scss', 'json', 'xml', 'sql'],
        'max_size': 5 * 1024 * 1024,  # 5MB
        'mime_types': ['text/x-python', 'application/javascript', 'text/x-java', 'text/x-c', 'text/html', 'text/css', 'application/json', 'application/xml']
    },
    'design': {
        'extensions': ['psd', 'ai', 'sketch', 'fig', 'xd', 'indd'],
        'max_size': 50 * 1024 * 1024,  # 50MB
        'mime_types': ['image/vnd.adobe.photoshop', 'application/postscript']
    },
    'audio': {
        'extensions': ['mp3', 'wav', 'ogg', 'aac', 'm4a', 'flac'],
        'max_size': 20 * 1024 * 1024,  # 20MB
        'mime_types': ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/aac', 'audio/flac']
    },
    'other': {
        'extensions': [],  # Catch-all
        'max_size': 25 * 1024 * 1024,  # 25MB
        'mime_types': []
    }
}


def get_file_extension(filename):
    """Extract file extension from filename."""
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def get_file_category(filename):
    """Determine file category based on extension."""
    ext = get_file_extension(filename)
    
    for category, config in FILE_CATEGORIES.items():
        if ext in config['extensions']:
            return category
    
    return 'other'


def validate_file_extension(filename):
    """
    Validate if file extension is allowed.
    Returns (is_valid, category, error_message)
    """
    ext = get_file_extension(filename)
    
    if not ext:
        return False, None, "File has no extension"
    
    # Check if extension is in any category
    for category, config in FILE_CATEGORIES.items():
        if ext in config['extensions']:
            return True, category, None
    
    # If not found in specific categories, allow as 'other'
    return True, 'other', None


def validate_file_size(file_size, category='other'):
    """
    Validate if file size is within allowed limits.
    Returns (is_valid, error_message)
    """
    if category not in FILE_CATEGORIES:
        category = 'other'
    
    max_size = FILE_CATEGORIES[category]['max_size']
    
    if file_size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        return False, f"File size exceeds {max_size_mb}MB limit for {category} files"
    
    return True, None


def generate_unique_filename(original_filename):
    """
    Generate a unique filename using timestamp and hash.
    Preserves original extension.
    """
    ext = get_file_extension(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create hash from original filename and timestamp
    hash_input = f"{original_filename}{timestamp}".encode('utf-8')
    file_hash = hashlib.md5(hash_input).hexdigest()[:8]
    
    return f"{timestamp}_{file_hash}.{ext}" if ext else f"{timestamp}_{file_hash}"


def get_upload_path(instance, filename):
    """
    Generate upload path for files.
    Structure: uploads/{category}/{year}/{month}/{unique_filename}
    """
    category = get_file_category(filename)
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    unique_filename = generate_unique_filename(filename)
    
    return os.path.join('uploads', category, year, month, unique_filename)


def validate_file(file):
    """
    Complete file validation.
    Returns (is_valid, category, errors)
    """
    errors = []
    
    # Validate extension
    is_valid_ext, category, ext_error = validate_file_extension(file.name)
    if not is_valid_ext:
        errors.append(ext_error)
        return False, None, errors
    
    # Validate size
    is_valid_size, size_error = validate_file_size(file.size, category)
    if not is_valid_size:
        errors.append(size_error)
    
    if errors:
        return False, category, errors
    
    return True, category, None


def format_file_size(size_bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
