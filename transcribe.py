# FILEPATH: c:/projects/python/transcribe.py

import os
import argparse
from faster_whisper import WhisperModel
from pydub import AudioSegment

def extract_audio(video_path, audio_path):
    """
    Extract audio from a video file and save it as an MP3 file.

    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path where the extracted audio will be saved.
    """
    audio = AudioSegment.from_file(video_path, format="mp4")
    audio.export(audio_path, format="mp3")

def validate_model(model_name):
    """
    Validate the provided Whisper model name.

    Args:
        model_name (str): The name of the Whisper model to validate.

    Returns:
        str: The validated model name.

    Raises:
        ValueError: If the provided model name is not in the list of available models.
    """
    available_models = ["tiny", "base", "small", "medium", "large"]
    if model_name not in available_models:
        raise ValueError(f"Invalid model name. Choose from: {', '.join(available_models)}")
    return model_name

def main(args):
    video_path = args.video_path
    audio_path = args.audio_path or os.path.splitext(video_path)[0] + ".mp3"
    transcription_path = args.transcription or os.path.splitext(video_path)[0] + ".txt"

    if args.force or not os.path.exists(audio_path):
        print("Extracting audio from video...")
        extract_audio(video_path, audio_path)

    print("Transcribing audio...")
    try:
        # Load the Whisper model
        model = WhisperModel(validate_model(args.model), device="auto", compute_type="auto")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Perform transcription
    segments, info = model.transcribe(audio_path, beam_size=5)
    transcription = " ".join(segment.text for segment in segments)

    # Save transcription to file
    print("Transcription complete. Saving to file...")
    with open(transcription_path, "w", encoding="utf-8") as f:
        f.write(transcription)

    # Remove temporary audio file if specified
    if args.remove_audio:
        print("Cleaning up temporary audio file...")
        os.remove(audio_path)

    print(f"Transcription saved to '{transcription_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio from a video file.")
    parser.add_argument("video_path", type=str, help="Path to the video file. Only accept MP4 at this moment.")
    parser.add_argument("-a", "--audio_path", type=str, help="Path to the audio file. Default is the same name as video_path with .mp3 extension.")
    parser.add_argument("-f", "--force", action="store_true", help="Force extract audio from video file. Default to False.")
    parser.add_argument("-r", "--remove_audio", action="store_true", help="Remove extracted audio file. Default to True.")
    parser.add_argument("-m", "--model", type=str, default="base", choices=["tiny", "base", "small", "medium", "large"], help="Whisper model. Default to 'base'.")
    parser.add_argument("-t", "--transcription", type=str, help="Transcription file name. Default to video_path with .txt extension.")

    args = parser.parse_args()
    main(args)