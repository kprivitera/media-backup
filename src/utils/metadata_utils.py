from PIL import Image
from PIL.ExifTags import TAGS
import subprocess
from pillow_heif import register_heif_opener
from datetime import datetime
import os

DATE_FORMAT = "%Y:%m:%d"

# Register HEIC support for Pillow
register_heif_opener()


def get_current_date():
    return datetime.now().strftime(DATE_FORMAT)


def get_file_creation_date(filepath):
    try:
        # Get the file's last modification time
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp).strftime(DATE_FORMAT)
    except Exception as e:
        print(f"Error retrieving file creation date: {e}")
        return None


def extract_image_metadata(filepath):
    metadata = {}
    try:
        with Image.open(filepath) as img:
            # General metadata
            metadata["info"] = img.info

            # EXIF metadata
            exif_data = img.getexif()
            if exif_data:
                metadata["exif"] = {
                    TAGS.get(tag, tag): value for tag, value in exif_data.items()
                }
            else:
                metadata["exif"] = None

    except Exception as e:
        metadata["error"] = f"Error extracting image metadata: {str(e)}"

    return metadata


def get_fallback_date(filepath):
    """
    Fallback logic to retrieve a date for a file.
    Tries the file creation/modification date, then falls back to the current date.
    """
    # Try to get the file creation/modification date
    file_date = get_file_creation_date(filepath)
    if file_date:
        return file_date

    # Final fallback to the current date
    return get_current_date()


def extract_image_date(filepath):
    print("regular image")
    metadata = extract_image_metadata(filepath)
    print(f"regular image metadata: {metadata}")

    # Try to get the date from EXIF metadata
    if metadata.get("exif"):
        date_str = metadata["exif"].get("DateTimeOriginal") or metadata["exif"].get(
            "DateTime"
        )
        if date_str:
            return date_str.split(" ")[0]  # Return only the date part (YYYY:MM:DD)

    # Use the fallback utility
    return get_fallback_date(filepath)


def extract_heic_date(filepath):
    try:
        # Open the HEIC file
        with Image.open(filepath) as img:
            # All metadata
            metadata = img.info

            # Check for EXIF metadata
            exif_data = img.getexif()

            if not exif_data:
                print("No EXIF metadata found.")
                return None

            # Check for DateTimeOriginal (36867) or fallback to DateTime (306)
            date_str = exif_data.get(36867) or exif_data.get(
                306
            )  # Use 306 as a fallback

            if not date_str:
                print("No valid date found in EXIF metadata.")
                return None

            # Parse the date string and return only the date part (YYYY:MM:DD)
            date_parts = date_str.split(" ")
            if len(date_parts) > 0:
                return date_parts[0]  # Return only the date part (YYYY:MM:DD)
    except Exception as e:
        print(f"Error extracting capture date: {str(e)}")
        return get_fallback_date(filepath)  # Use fallback utility


def extract_video_date(filepath):
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format_tags=creation_time",
                "-of",
                "default=noprint_wrappers=1",
                filepath,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for line in result.stdout.splitlines():
            if "creation_time" in line:
                return line.split("=")[1].split("T")[
                    0
                ]  # Return only the date part (YYYY-MM-DD)
    except Exception as e:
        print(f"Error extracting video date: {e}")
    return None


def get_date_by_file_type(file):
    """
    Process the file metadata based on its type.
    Returns the extracted date or an error message with a status code.
    """
    date = None

    if file.mimetype.startswith("image/"):
        if file.filename.lower().endswith(".heic"):
            date = extract_heic_date(file)
        else:
            date = extract_image_date(file)
    elif file.mimetype.startswith("video/"):
        date = extract_video_date(file)
        print(f"Video date: {date}")

    print(f"get_date_by_file_type: {date}")
    return str(date) if date else None
