import pygame
import pygame_gui
import sys
import re
import yt_dlp
import tkinter as tk
from tkinter import filedialog
import threading
import os

# Initialize Pygame
pygame.init()

# Set up the display
width, height = (500, 600)
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Social Media Video Downloader')

# Load images
Logo = pygame.image.load('assets/Logo.ico').convert()

pygame.display.set_icon(Logo)
yt_image = pygame.image.load('assets/Youtube_Logo.png').convert_alpha()
fb_image = pygame.image.load('assets/Facebook_Logo.png').convert_alpha()
tt_image = pygame.image.load('assets/TikTok_Logo.png').convert_alpha()
bg_image = pygame.image.load('assets/Background.png').convert()

# Create Pygame GUI manager
Manager = pygame_gui.UIManager((width, height))

# Create input boxes for URLs and buttons using Pygame GUI
yt_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 150), (300, 30)), manager=Manager)
fb_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 320), (300, 30)), manager=Manager)
tt_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 505), (300, 30)), manager=Manager)

yt_Download = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 190), (100, 30)), text='Download', manager=Manager)
fb_Download = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 360), (100, 30)), text='Download', manager=Manager)
tt_Download = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 545), (100, 30)), text='Download', manager=Manager)

# Load font
Label = ('fonts/SpaceGrotesk-Bold.ttf')
Label_text = pygame.font.Font(Label, 20)

# Create initial labels
yt_label = Label_text.render('Paste Youtube Video URL Here!', True, (255, 255, 255))  # White
yt_invalid_label = Label_text.render('Invalid Youtube video URL', True, (255, 0, 0))  # Red
fb_label = Label_text.render('Paste Facebook Video URL Here!', True, (255, 255, 255))
fb_invalid_label = Label_text.render('Invalid Facebook video URL', True, (255, 0, 0))
tt_label = Label_text.render('Paste Tiktok Video URL Here!', True, (255, 255, 255))
tt_invalid_label = Label_text.render('Invalid Tiktok video URL', True, (255, 0, 0))

# Clock to manage time in Pygame GUI
clock = pygame.time.Clock()

# Initialize the state for error display
error_start_time = None
current_error_label = None  # Label to display current error message
display_yt_label = True  # Flag to show/hide YouTube label
display_fb_label = True  # Flag to show/hide Facebook label
display_tt_label = True  # Flag to show/hide Tiktok label

# For YouTube
yt_progress = 0
yt_is_downloading = False
yt_show_download_complete_msg = False
yt_download_complete_time = 0

# For Facebook
fb_progress = 0
fb_is_downloading = False
fb_show_download_complete_msg = False
fb_download_complete_time = 0

# For TikTok
tt_progress = 0
tt_is_downloading = False
tt_show_download_complete_msg = False
tt_download_complete_time = 0


# Function to validate URL
def is_valid_url(url, platform):
    if platform == "YouTube":
        return re.match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+(&[\w=%-]+)?$', url)
    elif platform == "Facebook":
        return re.match(r'(https?://)?(www\.)?facebook\.com/watch/\?v=[\d]+$', url)
    elif platform == "TikTok":
        return re.match(r'(https?://)?(www\.)?tiktok\.com/@[\w.-]+/video/\d+$', url)
    return False


# Function to update the progress bar
def update_progress_bar(p, platform):
    if p['status'] == 'downloading':
        percent_str = re.sub(r'\x1b\[[0-9;]*m', '', p['_percent_str']).strip('%')
        try:
            progress_val = float(percent_str)
        except ValueError:
            progress_val = 0
        if platform == 'YouTube':
            global yt_progress
            yt_progress = progress_val
        elif platform == 'Facebook':
            global fb_progress
            fb_progress = progress_val
        elif platform == 'TikTok':
            global tt_progress
            tt_progress = progress_val
    
    if p['status'] == 'finished':
        if platform == 'YouTube':
            yt_progress = 100
        elif platform == 'Facebook':
            fb_progress = 100
        elif platform == 'TikTok':
            tt_progress = 100


def yt_video_download(url):
    global yt_is_downloading, yt_show_download_complete_msg, yt_download_complete_time
    save_path = filedialog.askdirectory()  # Ask the user for the download folder
    if save_path:  
        yt_is_downloading = True  # Start the download
        ydl_opts = {
            'format': 'bestvideo[height>=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Force 1080p+ MP4, or best quality MP4
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Save to the chosen directory with correct extension
            'progress_hooks': [lambda p: update_progress_bar(p, "YouTube")]  # Hook to update progress with platform
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # After download completion, show the download complete message
        yt_show_download_complete_msg = True
        yt_download_complete_time = pygame.time.get_ticks()  # Store the time when download is complete
    else:
        yt_is_downloading = False  # End the download if no folder is selected

    # Reset progress and downloading state after the download completes
    yt_is_downloading = False
    yt_progress = 0  # Reset the progress bar

def fb_video_download(url):
    global fb_is_downloading, fb_show_download_complete_msg, fb_download_complete_time
    save_path = filedialog.askdirectory()  # Ask the user for the download folder
    if save_path:  
        fb_is_downloading = True  # Start the download
        ydl_opts = {
            'format': 'bestvideo[height>=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Force 1080p+ MP4, or best quality MP4
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Save to the chosen directory with correct extension
            'progress_hooks': [lambda p: update_progress_bar(p, "Facebook")]  # Hook to update progress with platform
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # After download completion, show the download complete message
        fb_show_download_complete_msg = True
        fb_download_complete_time = pygame.time.get_ticks()  # Store the time when download is complete
    else:
        fb_is_downloading = False  # End the download if no folder is selected

    fb_is_downloading = False
    fb_progress = 0  # Reset the progress bar

def tt_video_download(url):
    global tt_is_downloading, tt_show_download_complete_msg, tt_download_complete_time
    save_path = filedialog.askdirectory()  # Ask the user for the download folder
    if save_path:  
        tt_is_downloading = True  # Start the download
        ydl_opts = {
            'format': 'bestvideo[height>=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Force 1080p+ MP4, or best quality MP4
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Save to the chosen directory with correct extension
            'progress_hooks': [lambda p: update_progress_bar(p, "TikTok")]  # Hook to update progress with platform
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        tt_show_download_complete_msg = True
        tt_download_complete_time = pygame.time.get_ticks()  # Store the time when download is complete
    else:
        tt_is_downloading = False  # End the download if no folder is selected

    tt_is_downloading = False
    tt_progress = 0  # Reset the progress bar

    
    
# Function to handle the download in a separate thread
def yt_download_thread(url):
    yt_video_download(url)
    
def fb_download_thread(url):
    fb_video_download(url)
    
def tt_download_thread(url):
    tt_video_download(url)


# Main loop
while True:
    time_delta = clock.tick(60) / 1000.0  # Ensures the program runs at 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Process Pygame GUI events
        Manager.process_events(event)

        # Handle button press events
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == yt_Download:
                yt_url = yt_input.get_text()
                if is_valid_url(yt_url, "YouTube"):
                    current_error_label = None  # No error
                    display_yt_label = True  # Show YouTube label
                    # Start the download in a new thread
                    threading.Thread(target=yt_download_thread, args=(yt_url,)).start()
                else:
                    current_error_label = yt_invalid_label  # Set error message
                    error_start_time = pygame.time.get_ticks()  # Get the current time
                    display_yt_label = False  # Hide YouTube label

            elif event.ui_element == fb_Download:
                fb_url = fb_input.get_text()
                if is_valid_url(fb_url, "Facebook"):
                    current_error_label = None  # No error
                    display_fb_label = True  # Show Facebook label
                    threading.Thread(target=fb_download_thread, args=(fb_url,)).start()
                else:
                    current_error_label = fb_invalid_label  # Set error message
                    error_start_time = pygame.time.get_ticks()
                    display_fb_label = False  # Hide Facebook label

            elif event.ui_element == tt_Download:
                tt_url = tt_input.get_text()
                if is_valid_url(tt_url, "TikTok"):
                    current_error_label = None  # No error
                    display_tt_label = True  # Show Tiktok label
                    threading.Thread(target=tt_download_thread, args=(tt_url,)).start()
                else:
                    current_error_label = tt_invalid_label  # Set error message
                    error_start_time = pygame.time.get_ticks()
                    display_tt_label = False  # Hide Tiktok label

    # Clear the display and draw the background and images
    display.blit(bg_image, (0, 0))
    display.blit(yt_image, (120, 50))
    display.blit(fb_image, (120, 230))
    display.blit(tt_image, (120, 380))

    # Draw the error label if it exists
    if current_error_label:
        if current_error_label == yt_invalid_label:
            display.blit(current_error_label, (125, 120))
        elif current_error_label == fb_invalid_label:
            display.blit(current_error_label, (125, 285))
        elif current_error_label == tt_invalid_label:
            display.blit(current_error_label, (125, 470))

    # Check if the error message should be removed after 2 seconds
    if current_error_label and (pygame.time.get_ticks() - error_start_time > 2000):  # 2 Seconds
        current_error_label = None  # Clear error label
        # Reset to show all labels again
        display_yt_label = True
        display_fb_label = True
        display_tt_label = True

    # Render the original prompt labels conditionally
    if display_yt_label:
        display.blit(yt_label, (100, 110))
    if display_fb_label:
        display.blit(fb_label, (100, 280))
    if display_tt_label:
        display.blit(tt_label, (110, 460))

    font_path = ('fonts/SpaceGrotesk-Bold.ttf')
    Top_label = pygame.font.Font(font_path, 15)
    
    # Update the progress bar
    if yt_is_downloading:
        progress_width = min(int(2 * yt_progress), 200)  # Cap the width at 200
        pygame.draw.rect(display, (214, 86, 214), (150, 137, progress_width, 10), border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)  # Pink progress fill
        pygame.draw.rect(display, (255, 255, 255), (150, 137, 200, 10), 1, 10, 10, 10, 10)  # Outline of the progress bar

    # Show "Video Downloaded" message for 3 seconds after download
    if yt_show_download_complete_msg:
        if pygame.time.get_ticks() - yt_download_complete_time < 3000:  # Show for 3 seconds
            Download_Complete = Top_label.render('Video Downloaded', True, (255, 255, 255))
            display.blit(Download_Complete, (173, 131))
        else:
            yt_show_download_complete_msg = False  # Hide the message after 3 seconds
            
            
    
    if fb_is_downloading:
        progress_width = min(int(2 * fb_progress), 200)  # Cap the width at 200
        pygame.draw.rect(display, (214, 86, 214), (150, 306, progress_width, 10), border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)  # Pink progress fill
        pygame.draw.rect(display, (255, 255, 255), (150, 306, 200, 10), 1, 10, 10, 10, 10)  # Outline of the progress bar


    # Show "Video Downloaded" message for 3 seconds after download
    if fb_show_download_complete_msg:
        if pygame.time.get_ticks() - fb_download_complete_time < 3000:  # Show for 3 seconds
            Download_Complete = Top_label.render('Video Downloaded', True, (255, 255, 255))
            display.blit(Download_Complete, (173, 301))
        else:
            fb_show_download_complete_msg = False  # Hide the message after 3 seconds
            
            
    if tt_is_downloading:
        progress_width = min(int(2 * tt_progress), 200)  # Cap the width at 200
        pygame.draw.rect(display, (214, 86, 214), (150, 488, progress_width, 10), border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)  # Pink progress fill
        pygame.draw.rect(display, (255, 255, 255), (150, 488, 200, 10), 1, 10, 10, 10, 10)  # Outline of the progress bar

    # Show "Video Downloaded" message for 3 seconds after download
    if tt_show_download_complete_msg:
        if pygame.time.get_ticks() - tt_download_complete_time < 3000:  # Show for 3 seconds
            Download_Complete = Top_label.render('Video Downloaded', True, (255, 255, 255))
            display.blit(Download_Complete, (173, 483))
        else:
            tt_show_download_complete_msg = False  # Hide the message after 3 seconds


    # Update the display
    Manager.update(time_delta)
    Manager.draw_ui(display)

    pygame.display.update()
