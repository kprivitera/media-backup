from PIL import Image
from PIL.ExifTags import TAGS
import subprocess
from pillow_heif import register_heif_opener
from datetime import datetime

# Register HEIC support for Pillow
register_heif_opener()


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


def extract_image_date(filepath):
    metadata = extract_image_metadata(filepath)

    if metadata.get("exif"):
        # Try to get DateTimeOriginal first
        date_str = metadata["exif"].get("DateTimeOriginal")
        if not date_str:
            # Fallback to DateTime if DateTimeOriginal is not available
            date_str = metadata["exif"].get("DateTime")

        if date_str:
            return date_str.split(" ")[0]  # Return only the date part (YYYY:MM:DD)

    return None


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

            # Parse the date string into a datetime object
            try:
                capture_date = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                return capture_date
            except ValueError:
                print(f"Error parsing date string: {date_str}")
                return None
    except Exception as e:
        print(f"Error extracting capture date: {str(e)}")
        return None


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

    return str(date) if date else None
