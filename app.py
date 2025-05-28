import os
import subprocess
import whisper
import streamlit as st

# Ensure ffmpeg is installed
FFMPEG_PATH = "ffmpeg"  # Update this path if necessary

# Function to download video
def download_video(url, output="video.mp4"):
    try:
        command = f'yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o {output} "{url}"'
        subprocess.run(command, shell=True, check=True)
        return output
    except subprocess.CalledProcessError:
        st.error("Error downloading the video. Please check the URL or try a different video.")
        return None

# Extract audio using ffmpeg
def extract_audio(video_path, output="audio.wav"):
    try:
        command = f'{FFMPEG_PATH} -i {video_path} -vn -acodec pcm_s16le -ar 16000 {output}'
        subprocess.run(command, shell=True, check=True)
        return output
    except subprocess.CalledProcessError:
        st.error("Error extracting audio. Ensure ffmpeg is installed correctly.")
        return None

# Transcribe and analyze accent
def analyze_accent(audio_path):
    try:
        model = whisper.load_model("small")
        result = model.transcribe(audio_path)
        text = result["text"]
        
        # Mock accent classification (Replace with trained model for better accuracy)
        accent = "American" if "r" in text else "British"
        confidence = 85 if accent == "American" else 75
        
        return accent, confidence, text
    except Exception as e:
        st.error(f"Error analyzing audio: {e}")
        return None, None, None

# Streamlit UI
def main():
    st.title("English Accent Detection Tool")
    url = st.text_input("Enter video URL (YouTube or MP4):")

    if st.button("Analyze"):
        if not url:
            st.error("Please provide a valid video URL.")
            return

        st.write("Downloading video...")
        video_path = download_video(url)
        if not video_path:
            return

        st.write("Extracting audio...")
        audio_path = extract_audio(video_path)
        if not audio_path:
            return

        st.write("Analyzing accent...")
        accent, confidence, summary = analyze_accent(audio_path)
        
        if accent:
            st.write(f"**Detected Accent:** {accent}")
            st.write(f"**Confidence Score:** {confidence}%")
            st.write(f"**Transcription:** {summary}")

if __name__ == "__main__":
    main()
