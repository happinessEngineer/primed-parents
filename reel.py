import openai
import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from datetime import datetime
from textwrap import wrap
from PIL import Image as PILImage
import math

# --- CONFIG ---
# AFFIRMATION = "I appreciate the sacred dance of parenthood and the endless wells of love it reveals."
AFFIRMATION = "Oh, I love the way my breath anchors me in this moment of peace."
VOICE = "onyx"
FONT_PATH = "Quicksand-VariableFont_wght.ttf"  # Update this to your actual font file path
FONT_SIZE = 90
WIDTH, HEIGHT = 1080, 1920
TEXT_COLOR = "#222222"
BG_COLOR = (204, 255, 204)  # Pastel green
FPS = 24
OUTPUT_DIR = "output_frames"
AUDIO_PATH = "voiceover.mp3"
VIDEO_PATH = "synced_affirmation.mp4"

instructions = """Voice Affect: Deep, appreciative, gentle, soothing; embody tranquility.\n\nTone: Calm, reassuring, peaceful; convey genuine warmth and serenity.\n\nPacing: Slow, deliberate, and unhurried; pause gently after instructions to allow the listener time to relax and follow along.\n\nEmotion: Deeply soothing and comforting; express genuine kindness and care.\n\nPronunciation: Smooth, soft articulation, slightly elongating vowels to create a sense of ease.\n\nPauses: Use thoughtful pauses, especially between breathing instructions and visualization guidance, enhancing relaxation and mindfulness."""

# --- OPENAI TTS ---
print("Generating voiceover from OpenAI...")
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.audio.speech.create(
    model="tts-1-hd",
    voice=VOICE,
    input=AFFIRMATION,
    response_format="mp3",
    instructions=instructions
)

# Save the audio file
audio_bytes = response.read()
with open(AUDIO_PATH, "wb") as f:
    f.write(audio_bytes)

# --- ESTIMATE TIMESTAMPS ---
print("Estimating word timings...")
words = AFFIRMATION.split()
total_words = len(words)

audio_clip = AudioFileClip(AUDIO_PATH)
audio_duration = audio_clip.duration
print(f"Audio duration: {audio_duration:.2f}s")

# Evenly distribute timing across all words
segments = []
current_time = 0.0
for word in words:
    segment_duration = audio_duration / total_words
    segments.append({
        "text": word,
        "start": current_time,
        "end": current_time + segment_duration
    })
    current_time += segment_duration

# --- GENERATE FRAMES ---
print("Generating image frames...")
os.makedirs(OUTPUT_DIR, exist_ok=True)

frame_count = 0
frames = []
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font.set_variation_by_axes([600])  # Set weight to 600 (semi-bold for main text)
watermark_font = ImageFont.truetype(FONT_PATH, 54)
watermark_font.set_variation_by_axes([600])  # Set weight to 600 (semi-bold for main text)
moodreset_font = ImageFont.truetype(FONT_PATH, 64)
moodreset_font.set_variation_by_axes([700])  # Use boldest weight available

# Load lightning bolt image for header
lightning_img = PILImage.open("noun-lightning-bolt-9594-FFB258.png").convert("RGBA")

# Helper function to wrap text to fit image width
def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + (' ' if current_line else '') + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# --- Precompute the full text block size for centering ---
full_text = AFFIRMATION
img_for_measure = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw_for_measure = ImageDraw.Draw(img_for_measure)
full_lines = wrap_text(full_text, font, WIDTH * 0.9, draw_for_measure)
full_text_heights = [draw_for_measure.textbbox((0, 0), line, font=font)[3] - draw_for_measure.textbbox((0, 0), line, font=font)[1] for line in full_lines]
full_text_height = sum(h * 2 for h in full_text_heights)
full_text_width = max([draw_for_measure.textbbox((0, 0), line, font=font)[2] - draw_for_measure.textbbox((0, 0), line, font=font)[0] for line in full_lines])

# Build up the phrase word by word
cumulative_phrase = []
for idx, seg in enumerate(segments):
    word = seg["text"]
    start = seg["start"]
    end = seg["end"]
    duration = end - start
    num_frames = int(duration * FPS)
    cumulative_phrase.append(word)
    text_to_show = " ".join(cumulative_phrase)

    for i in range(num_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)
        lines = wrap_text(text_to_show, font, WIDTH * 0.9, draw)
        y_offset = (HEIGHT - full_text_height) / 2
        # Find the current word's index in the lines
        current_word_index = len(cumulative_phrase) - 1
        word_counter = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            words_in_line = line.split()
            x_offset = (WIDTH - w) / 2
            word_x = x_offset
            for j, w_in_line in enumerate(words_in_line):
                if word_counter == current_word_index:
                    # Draw a white rounded rectangle behind the current word
                    # Get word bbox at (0, 0) for width/height
                    word_bbox_local = draw.textbbox((0, 0), w_in_line, font=font)
                    word_w = word_bbox_local[2] - word_bbox_local[0]
                    word_h = word_bbox_local[3] - word_bbox_local[1]
                    pad_x = 16
                    pad_y = 8
                    rect_x0 = word_x - pad_x
                    rect_y0 = y_offset + word_bbox_local[1] - pad_y
                    rect_x1 = word_x + word_w + pad_x
                    rect_y1 = y_offset + word_bbox_local[3] + pad_y
                    draw.rounded_rectangle([rect_x0, rect_y0, rect_x1, rect_y1], radius=word_h//2, fill="white")
                    # Draw main word
                    draw.text((word_x, y_offset), w_in_line, font=font, fill=TEXT_COLOR)
                else:
                    draw.text((word_x, y_offset), w_in_line, font=font, fill=TEXT_COLOR)
                word_bbox = draw.textbbox((word_x, y_offset), w_in_line, font=font)
                word_w = word_bbox[2] - word_bbox[0]
                word_x += word_w + draw.textlength(' ', font=font)
                word_counter += 1
            y_offset += h * 2
        # Add watermark at the bottom (unchanged)
        watermark_text = "Primed Parents"
        watermark_bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
        watermark_w = watermark_bbox[2] - watermark_bbox[0]
        watermark_h = watermark_bbox[3] - watermark_bbox[1]
        watermark_x = (WIDTH - watermark_w) / 2
        watermark_y = HEIGHT - watermark_h - 120  # 120px padding from bottom (moved up)
        draw.text((watermark_x, watermark_y), watermark_text, font=watermark_font, fill=TEXT_COLOR)
        # Add 'Mood Reset' with lightning images at the top
        moodreset_text = "Mood Reset"
        moodreset_bbox = draw.textbbox((0, 0), moodreset_text, font=moodreset_font)
        moodreset_w = moodreset_bbox[2] - moodreset_bbox[0]
        moodreset_h = moodreset_bbox[3] - moodreset_bbox[1]
        icon_h = moodreset_h
        icon_w = int(lightning_img.width * (icon_h / lightning_img.height))
        lightning_resized = lightning_img.resize((icon_w, icon_h), PILImage.LANCZOS)
        gap = 24
        total_header_w = icon_w + gap + moodreset_w + gap + icon_w
        header_x = (WIDTH - total_header_w) / 2
        header_y = 60
        # Add a full-width white rectangle behind the header (squared corners, starts at top)
        rect_height = int(header_y + icon_h + (header_y))
        rect_y0 = 0
        rect_y1 = rect_height
        draw.rectangle([(0, rect_y0), (WIDTH, rect_y1)], fill="white")
        bolt_y = int(header_y + 12)
        # Paste left lightning (no rotation)
        img.paste(lightning_resized, (int(header_x), bolt_y), lightning_resized)
        text_x = header_x + icon_w + gap
        draw.text((text_x, header_y), moodreset_text, font=moodreset_font, fill=TEXT_COLOR)
        # Paste right lightning (no rotation)
        img.paste(lightning_resized, (int(text_x + moodreset_w + gap), bolt_y), lightning_resized)
        frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame_count:04d}.png")
        img.save(frame_path)
        frames.append(frame_path)
        frame_count += 1

# Add a final slide with all text and no outline, lasting 2 seconds
final_frames = int(2 * FPS)
for i in range(final_frames):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    lines = wrap_text(AFFIRMATION, font, WIDTH * 0.9, draw)
    y_offset = (HEIGHT - full_text_height) / 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((WIDTH - w) / 2, y_offset), line, font=font, fill=TEXT_COLOR)
        y_offset += h * 2
    # Add watermark at the bottom
    watermark_text = "Primed Parents"
    watermark_bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    watermark_w = watermark_bbox[2] - watermark_bbox[0]
    watermark_h = watermark_bbox[3] - watermark_bbox[1]
    watermark_x = (WIDTH - watermark_w) / 2
    watermark_y = HEIGHT - watermark_h - 120  # 120px padding from bottom (moved up)
    draw.text((watermark_x, watermark_y), watermark_text, font=watermark_font, fill=TEXT_COLOR)
    # Add 'Mood Reset' with lightning images at the top
    moodreset_text = "Mood Reset"
    moodreset_bbox = draw.textbbox((0, 0), moodreset_text, font=moodreset_font)
    moodreset_w = moodreset_bbox[2] - moodreset_bbox[0]
    moodreset_h = moodreset_bbox[3] - moodreset_bbox[1]
    icon_h = moodreset_h
    icon_w = int(lightning_img.width * (icon_h / lightning_img.height))
    lightning_resized = lightning_img.resize((icon_w, icon_h), PILImage.LANCZOS)
    gap = 24
    total_header_w = icon_w + gap + moodreset_w + gap + icon_w
    header_x = (WIDTH - total_header_w) / 2
    header_y = 60
    # Add a full-width white rectangle behind the header (squared corners, starts at top)
    rect_height = int(header_y + icon_h + (header_y))
    rect_y0 = 0
    rect_y1 = rect_height
    draw.rectangle([(0, rect_y0), (WIDTH, rect_y1)], fill="white")
    bolt_y = int(header_y + 12)
    # No rotation for final slide
    img.paste(lightning_resized, (int(header_x), bolt_y), lightning_resized)
    text_x = header_x + icon_w + gap
    draw.text((text_x, header_y), moodreset_text, font=moodreset_font, fill=TEXT_COLOR)
    img.paste(lightning_resized, (int(text_x + moodreset_w + gap), bolt_y), lightning_resized)
    frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame_count:04d}.png")
    img.save(frame_path)
    frames.append(frame_path)
    frame_count += 1

# --- COMPILE VIDEO ---
print("Compiling video...")
clip = ImageSequenceClip(frames, fps=FPS).with_audio(audio_clip)
clip.write_videofile(VIDEO_PATH, fps=FPS)

print(f"\n✅ Video created: {VIDEO_PATH}")