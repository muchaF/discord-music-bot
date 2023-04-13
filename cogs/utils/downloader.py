from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import os 


class Downloader(YoutubeDL):
    ydl_opts = {
        'noplaylist' : True,                
        #'playlistend' : '1',                # skip playlist after first song 
        'quiet' : True,
        'format': 'bestaudio/best',
        'paths' : {
            'home' : '/songs',
            'temp' : '/songs/temp'
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            #'preferredcodec': 'mp3',       # conversion taking too long
            'preferredquality': '192',
        }],
    }

    def __init__(self, ydl_options = ydl_opts):
        super().__init__(ydl_options)
        try:
            self.download_path = ydl_options['paths']['home']

            # removing "/" at at beginning
            if self.download_path[0] == '/': 
                self.download_path = self.download_path[1:]
            # adding "/" to the end
            if self.download_path[-1] != '/':
                self.download_path += '/'

        except KeyError:
            self.download_path = ''

    def download(self, link, name=''):
        info = self.extract_info(link, download=True)

        # if playlist 
        if 'entries' in info.keys():
            info = info['entries'][0]

        file_path = info['requested_downloads'][0]['filepath']
        
        file = file_path.split("\\")[-1]

        if name == '':
            return info, file
        else:
            file_type = file.split(".")[-1]
            new_file_path = f"{self.download_path}{name}.{file_type}"
            # remove file with same name
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            os.rename(f"{self.download_path}{file}", new_file_path)
            return info, f"{name}.{file_type}"



if __name__ == "__main__":
    links = [
    "https://music.youtube.com/watch?v=fTX8E4pkMpU&list=RDAMVMfTX8E4pkMpU",
    "https://www.youtube.com/watch?v=qrFdCuOi5n8&ab_channel=lilbubblegum-Topic",
    # "https://soundcloud.com/user-358871701",
    "https://music.youtube.com/watch?v=1TDdhMqKZQU&list=PL10cLkk1BRwmZ6iXzvB9G41aGSA6EjLY_",
    "https://soundcloud.com/gammaraystorm/mgmt-little-dark-age-slowed"
    ]

    

    DLer = Downloader()
    # for index, link in enumerate([links[3]]):
    for index, link in enumerate(links):
        try:
            info, _ = DLer.download(link, name=str(index))
            try:
                # print(info['duration'])
                # print(info['title'])
                # print(info['thumbnail'])
                print(info['uploader'])
                print(info['uploader_url'])
                print(info['extractor_key'])

                # for key in info.keys():
                #     s = f"{key} : {info[key]}"
                #     print('%.3000s' % s) 
                print("-"*30)
            except KeyError:
                print("key error")
        except Exception as e:
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")



# Traceback (most recent call last):
#   File "c:\Users\Filip\Desktop\discord_bot_v2\cogs\utils\downloader.py", line 75, in <module>
#     info, _ = DLer.download(link, name=str(index))
#   File "c:\Users\Filip\Desktop\discord_bot_v2\cogs\utils\downloader.py", line 38, in download
#     info = self.extract_info(link, download=True)
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1507, in extract_info
#     return self.__extract_info(url, self.get_info_extractor(key), download, extra_info, process)
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1518, in wrapper
#     return func(self, *args, **kwargs)
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1615, in __extract_info
#     return self.process_ie_result(ie_result, download, extra_info)
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1744, in process_ie_result
#     return self.__process_playlist(ie_result, download)
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1888, in __process_playlist
#     entry_result = self.__process_iterable_entry(entry, download, collections.ChainMap({
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1518, in wrapper
#     return func(self, *args, **kwargs)
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1920, in __process_iterable_entry
#     return self.process_ie_result(
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1694, in process_ie_result
#     return self.extract_info(
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1507, in extract_info
#     return self.__extract_info(url, self.get_info_extractor(key), download, extra_info, process)
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1536, in wrapper
#     self.report_error(str(e), e.format_traceback())
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 1015, in report_error
#     self.trouble(f'{self._format_err("ERROR:", self.Styles.ERROR)} {message}', *args, **kwargs)
#   File "C:\Users\Filip\AppData\Local\Programs\Python\Python310\lib\site-packages\yt_dlp\YoutubeDL.py", line 955, in trouble
#     raise DownloadError(message, exc_info)
# yt_dlp.utils.DownloadError: ERROR: [youtube] qrFdCuOi5n8: Video unavailable. This video is not available