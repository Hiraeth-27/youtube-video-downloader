import customtkinter
from pathlib import Path
from threading import Thread
from pytube import YouTube, Playlist
from pytube.exceptions import ExtractError, HTMLParseError, LiveStreamError, MaxRetriesExceeded, VideoUnavailable
import time

customtkinter.set_appearance_mode('dark')
download = Thread()

class LinkFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text='Enter Youtube Link: ')
        self.label.grid(row=0, column=0, padx=10, pady=(10, 10))
        
        self.link_textbox = customtkinter.CTkTextbox(self, height=10)
        self.link_textbox.grid(row=0, column=1, padx=10, pady=10)

    def get(self):
        return self.link_textbox.get('0.0', 'end')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('Youtube Video Downloader')
        self.geometry('600x400')
        
        self.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(self, text='Youtube Video Downloader')
        self.title_label.grid(row=0, column=0, sticky='ew', pady=10)

        self.link_frame = LinkFrame(self)
        self.link_frame.grid(row=1, column=0, pady=10)

        self.button = customtkinter.CTkButton(self, text='Download', command=self.download_button_callback)
        self.button.grid(row=2, column=0, pady=10)

        self.video_title_label = customtkinter.CTkLabel(self, text='Downloading: ')
        self.video_title_label.grid(row=3, column=0, pady=10)

        self.progress_frame = customtkinter.CTkFrame(self)
        self.progress_frame.grid(row=4, column=0, pady=10)

        self.progress_bar = customtkinter.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=4, column=0, padx=10, pady=10)

        self.percentage_label = customtkinter.CTkLabel(self.progress_frame, text='0%')
        self.percentage_label.grid(row=4, column=1, padx=10, pady=10)


    def download_button_callback(self):
        download = Thread(target = self.download)
        download.start()
        self.button.configure(state='disabled')

    def download(self):
        self.num_videos = 1
        self.downloaded_videos = 0
        url = self.link_frame.get()

        download_path = str(Path.home()) + '/Downloads'
        self.video_title_label.configure(text=f'Downloading: {url}')

        if ('playlist' in url):
            playlist = Playlist(url)
            self.num_videos = playlist.length
            self.button.configure(state='disabled')
            for video in playlist.videos:
                try:
                    video.register_on_progress_callback(self.on_download_progress)
                    self.video_title_label.configure(text=f'Downloading: {video.title} | ({self.downloaded_videos + 1}/{self.num_videos})')
                    video.streams.get_highest_resolution().download(download_path + f'/{playlist.title}', max_retries=5)
                    self.downloaded_videos += 1
                except ExtractError:
                    self.video_title_label.configure(text='Extract error, skipping...')
                    time.sleep(3)
                except HTMLParseError:
                    self.video_title_label.configure(text='HTML parse error, skipping...')
                    time.sleep(3)
                except LiveStreamError:
                    self.video_title_label.configure(text=f'{video.title} is a livestream, skipping...')
                    time.sleep(3)
                except MaxRetriesExceeded:
                    self.video_title_label.configure(text=f'Max retries exceeded, skipping...')
                    time.sleep(3)
                except VideoUnavailable:
                    self.video_title_label.configure(text=f'{video.title} is unavailalbe, skipping...')
                    time.sleep(3)
        else:
            try:
                yt = YouTube(url, on_progress_callback=self.on_download_progress)
                self.video_title_label.configure(text=f'Downloading: {yt.title} | ({self.downloaded_videos + 1}/{self.num_videos})')
                yt.streams.get_highest_resolution().download(download_path, max_retries=5)
            except ExtractError:
                self.video_title_label.configure(text='Extract error, skipping...')
                time.sleep(3)
            except HTMLParseError:
                self.video_title_label.configure(text='HTML parse error, skipping...')
                time.sleep(3)
            except LiveStreamError:
                self.video_title_label.configure(text=f'{yt.title} is a livestream, skipping...')
                time.sleep(3)
            except MaxRetriesExceeded:
                self.video_title_label.configure(text=f'Max retries exceeded, skipping...')
                time.sleep(3)
            except VideoUnavailable:
                self.video_title_label.configure(text=f'{yt.title} is unavailalbe, skipping...')
                time.sleep(3)

        if (not download.is_alive()):
            self.button.configure(state='normal')
            self.video_title_label.configure(text='DOWNLOAD COMPLETED')

    def on_download_progress(self, stream, chunk, bytes_remaining):
        size = stream.filesize

        progress = (size - bytes_remaining) / size
        self.percentage_label.configure(text=f'{round(progress * 100, 2)}%')
        self.progress_bar.set(progress)



        
    
app = App()
app.mainloop()