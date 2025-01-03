import gradio as gr
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

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Video Screenshot Extractor")
    gr.Markdown("Upload a video and specify a timestamp to extract a screenshot from that moment.")
    with gr.Row():
        video_input = gr.Video(label="Upload Video")
        timestamp_input = gr.Number(label="Timestamp (seconds)", value=0)
    screenshot_output = gr.Image(label="Screenshot")
    
    extract_button = gr.Button("Extract Screenshot")
    extract_button.click(fn=extract_screenshot, inputs=[video_input, timestamp_input], outputs=screenshot_output)

if __name__ == "__main__":
    demo.launch()
