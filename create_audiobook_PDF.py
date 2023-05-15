# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 18:47:16 2023

@author: Rizwan Hassan
"""
import boto3
from pydub import AudioSegment
import fitz

aws_access_key_id='ABCDEGHIJKLMO'
aws_secret_access_key='ABCDEGHIJKLMO'

# Open the PDF file
pdf_doc = fitz.open(r"path/to/pdf-book.pdf")
#pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Define the page numbers of the first chapter
start_page = 5
end_page = 7

# Extract the text from the pages of the first chapter
text = ""
for page_num in range(start_page, end_page):
    page = pdf_doc[page_num]
    text += page.get_text("text")
# Close the PDF file
pdf_doc.close()

# Convert the text to speech using Amazon Polly
def text_to_speech(text, aws_access_key_id, aws_secret_access_key):
    polly = boto3.client("polly",
        region_name="us-west-2",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # Divide the text into smaller chunks
    chunk_size = 1500  # This is the maximum size of the text that can be synthesized in a single request
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # Synthesize the audio for each chunk
    audio_chunks = []
    for chunk in chunks:
        response = polly.synthesize_speech(
            Text=chunk,
            OutputFormat="mp3",
            VoiceId="Joanna"
        )
        audio_chunks.append(response["AudioStream"].read())

    # Combine the audio chunks
    combined = b"".join(audio_chunks)
    with open("Proust_audio_book.mp3", "wb") as f:
        f.write(combined)

text_to_speech(text, aws_access_key_id, aws_secret_access_key)

# Load the background music file
music = AudioSegment.from_file(r"path/to/audio/file/to/add/background/music/audio1.mp3")

# Set the volume of the background music to moderate
music = music.apply_gain(-10.0)

# Load the audio book file
audio_book = AudioSegment.from_file("Proust_audio_book.mp3")

# Combine the two audio files and set the volume of the background music to moderate
combined = audio_book.overlay(music)

# Save the combined audio file
combined.export(r"audio_book_with_music.mp3", format="mp3")
# Play the combined audio file

