import os
import subprocess
import whisper
# Define ffmpeg path (adjust for deployment)
FFMPEG_PATH = "ffmpeg"  

# Function to download video
def download_video(url, output="video.mp4"):
    try:
        command = f'yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o {output} "{url}"'
        subprocess.run(command, shell=True, check=True)
        return output
    except subprocess.CalledProcessError:
        st.error("Error downloading video. Please check the URL and try again.")
        return None

# Extract audio from video
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

        # Basic accent classification logic (can be improved with AI models)
        american_keywords = ["r", "er", "ar"]
        british_keywords = ["ah", "o", "ou"]

        american_count = sum(text.lower().count(k) for k in american_keywords)
        british_count = sum(text.lower().count(k) for k in british_keywords)

        if american_count > british_count:
            accent = "American"
            confidence = min(100, (american_count / (american_count + british_count)) * 100)
        else:
            accent = "British"
            confidence = min(100, (british_count / (american_count + british_count)) * 100)

        summary = f"The detected accent has strong {'r' if accent == 'American' else 'ah'} sounds, common in {accent} English."
        return accent, confidence, summary
    except Exception as e:
        st.error(f"Error analyzing audio: {e}")
        return None, None, None

# Streamlit UI
def main():
    st.title("English Accent Detection Tool")
    url = st.text_input("Enter video URL (YouTube, Loom, MP4):")

    if st.button("Analyze"):
        if not url:
            st.error("Please enter a valid video URL.")
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
            st.write(f"**Confidence Score:** {confidence:.2f}%")
            st.write(f"**Summary:** {summary}")

if __name__ == "__main__":
    main()
