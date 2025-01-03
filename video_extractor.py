import subprocess
import os
from PIL import Image
import tempfile

def extract_screenshot(video_file, timestamp):
    """
    Extract a screenshot from a video at the specified timestamp using ffmpeg
    """
    if not video_file:
        return None
    
    # Create a temporary file for the screenshot
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        output_path = tmp_file.name

    try:
        # Use ffmpeg to extract the frame
        command = [
            'ffmpeg',
            '-ss', str(timestamp),  # Seek to timestamp
            '-i', video_file,  # Input file path (now a string)
            '-vframes', '1',        # Extract one frame
            '-q:v', '2',           # High quality
            '-y',                  # Overwrite output file if it exists
            output_path
        ]
        
        # Run ffmpeg and capture its output
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return None

        # Check if the output file exists and has size
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            print(f"Output file is empty or doesn't exist")
            return None

        # Try to open the image
        try:
            screenshot = Image.open(output_path)
            return screenshot
        except Exception as e:
            print(f"Error opening image: {e}")
            return None
            
    except Exception as e:
        print(f"Error extracting screenshot: {e}")
        return None
    finally:
        # Clean up the temporary file
        if os.path.exists(output_path):
            os.unlink(output_path)
