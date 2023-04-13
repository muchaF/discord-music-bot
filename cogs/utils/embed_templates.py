from discord import Embed, File


def time_string(duration):
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    if  m == 0 and h == 0:
        return f"{s}s"
    elif h == 0:
        return "{:d}:{:02d}".format(m, s)
    else:
        return "{:d}:{:02d}:{:02d}".format(h, m, s)


class EmbedTemplates:
    colors = {
        "green" : 5763719,
        "red" : 15548997,
        "Youtube" : 16711680,
        "Soundcloud" : 16742144
    }

    # images = {
    #     "Youtube" : discord.File('path/to/example.png', filename='example.png')  
    #     "Soundcloud" :  
    # }

    @staticmethod
    def song_large(song, queue):
        color = EmbedTemplates.colors[song.extractor_key]
        return Embed.from_dict(
            {
            'thumbnail': {
                'url': song.thumbnail
                }, 
            'author': {
                'name': "🎵 Song added to queue",
                }, 
            'fields': [
                {'inline': True, 'name': '| Author', 
                    'value': f"{song.uploader}"}, 
                {'inline': True, 'name': '| Duration', 
                    'value': f"{time_string(song.duration)}"},
                {'inline': False, "name": "", "value": ""},
                {'inline': True, 'name': '| Queue length', 
                    'value': f"{queue.lenght()}"}, 
                {'inline': True, 'name': '| Queue duration', 
                    'value': time_string(queue.time_left)}
                ], 
            'color': color, 
            'type': 'rich', 
            'url': f"{song.url}", 
            'title': f"{song.title}",
            'footer': {
                'text': f"Requested by {song.requester_nick}",
                'icon_url': f"{song.requester_avatar_url}"
                }
            }
        )

    def song_small(song):
        color = EmbedTemplates.colors[song.extractor_key]
        return Embed.from_dict(
            {
            'title': f"{song.title}",
            'url': f"{song.url}", 
            'thumbnail': {
                'url': song.thumbnail
                }, 
            'fields': [
                {'inline': True, 'name': "│ " + song.uploader, 
                    'value': ""}, 
                {'inline': True, 'name': f"│ {time_string(song.duration)}", 
                    'value': ""}, 
                ], 
            'color': color, 
            'type': 'rich', 
            }
        )

    @staticmethod
    def generic_text(text, color='green'):
        color = EmbedTemplates.colors[color]

        return Embed.from_dict({
            "type": "rich",
            "description": "",
            "color": color,
            "fields": [
                {
                "name": f"{text}",
                "value": "",
                "inline": True
                }],
        })
    

    @staticmethod
    def help():
        color = EmbedTemplates.colors["green"]
        help_hover = \
"""
┌────────────────────────────────────────────────────────────────────
├─── !play [!p] <args>
│ přehraje/přidá písničku do fronty, argument muže být odkaz na 
│ YouTube, SoundCloud, nebo slova pro vyhledávání na YouTubu
├─── !pause 
│ pozastaví/obnoví přehrávání
├─── !resume  
│ obnoví přehrávání
├─── !skip [!s]  
│ přeskočí aktuálně přehrávanou písničku
├─── !remove_last  
│ odstraní poslední přidanou písníčku z fronty
├─── !help [!info] 
│ zobrazí tuto tabulku
└────────────────────────────────────────────────────────────────────
"""
        return Embed.from_dict(
            {
            'title': f"Music bot Ferko",
            'fields': [
                {'inline': True, 'name': "│ Commands", 
                    'value': f'[[Hover for commands]](https://www. "{help_hover}")'
                },
                {'inline': False, 'name': "│ Links", 
                    'value': f'[__GitHub__](https://github.com/muchaF)'
                }
                ], 
            'thumbnail' : {
                'url' : "https://cdn.discordapp.com/avatars/893805512670461972/67bf7c3ba6ad7119480b0bc14ce06d59.webp"
            },
            'color': color, 
            'type': 'rich',
            'footer': {
                'text': "Created by Filip M.",
                'icon_url': "https://cdn.discordapp.com/avatars/534429464143069185/31524125bddf760a64c8c9a698a0cd71.webp"
                }
            }
        )

