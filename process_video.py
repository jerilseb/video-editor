import os
import openai
import shutil
from dotenv import load_dotenv
from prompt import system_prompt

load_dotenv()


def process_video(video_file, edit_instructions):
    """
    Process a video file based on edit instructions using OpenAI API to generate ffmpeg commands.
    """
    if not video_file or not edit_instructions:
        return None

    if not os.path.exists(video_file):
        print(f"Input file {video_file} does not exist.")
        return None

    # Call OpenAI API to get ffmpeg command
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"Generate an ffmpeg command to {edit_instructions}.",
            },
        ],
        max_tokens=250,
    )

    ffmpeg_command = response.choices[0].message.content
    ffmpeg_command = ffmpeg_command.strip().replace("input.mp4", video_file)
    print(ffmpeg_command)

    # Remove and recreate the outputs directory
    output_dir = "outputs"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    try:
        # Execute the ffmpeg command
        os.system(ffmpeg_command)

        # Check for .mp4 files in the outputs directory
        output_files = [f for f in os.listdir(output_dir) if f.endswith('.mp4')]
        if not output_files:
            print("No .mp4 files found in the outputs directory.")
            return None

        output_path = os.path.join(output_dir, output_files[0])
        if os.path.getsize(output_path) == 0:
            print("Output file is empty.")
            return None

        return output_path

    except Exception as e:
        print(f"Error processing video: {e}")
        return None
