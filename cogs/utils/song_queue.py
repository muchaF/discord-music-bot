class Song:
    def __init__(self, file, url, author_nick, author_avatar_url, info):
        self.file = file
        self.url = url
        self.duration = int(info['duration'])
        self.title = info['title']
        self.thumbnail = info['thumbnail']
        self.uploader = info['uploader']
        self.uploader_url = info['uploader_url']
        self.extractor_key = info['extractor_key']
        
        self.requester_nick = author_nick
        self.requester_avatar_url = author_avatar_url

    def __str__(self):
        return "\n".join(
            f'{key} : {value}' for (key, value) in self.__dict__.items())


class Queue():
    def __init__(self):
        self.song_list = []
        self.time_left = 0

    def lenght(self):
        return len(self.song_list)

    def add(self, song, first=False):
        self.time_left += song.duration
        if first:
            self.song_list.insert(0, song)
        else:
            self.song_list.append(song)
    
    def pop(self, index):
        song = self.song_list.pop(index)
        if len(self.song_list) == 0:
            self.time_left = 0
        else:
            self.time_left -= song.duration
        return song


if __name__ == "__main__":
    q = Queue()
    q.time_left = 32
    print(q.time_left_str()) 
    q.time_left = 435
    print(q.time_left_str())
    q.time_left = 123123
    print(q.time_left_str())
    