import re, urllib.parse, urllib.request


class LinkProcessing:
    @staticmethod
    def relevantLink(key_words):
        _query_YT = 'https://www.youtube.com/results?search_query='
        _result_YT = 'https://www.youtube.com/watch?v='
        _regex_id = r'\/watch\?v=([a-zA-Z0-9_\-]{11})'

        key_words = [*key_words]
        for i in range(len(key_words)):
            key_words[i] = urllib.parse.quote(key_words[i])

        # make query link
        query_link = _query_YT + '+'.join(key_words)
        # get id of first video from result
        html = urllib.request.urlopen(query_link).read().decode()
        video_id = re.search(_regex_id, html).group(1)
        # video_id = re.findall(r"(?<=/watch\?v=)(\S{11})", html)[0]
        video_link = _result_YT + video_id

        return video_link


    @staticmethod
    def process(args):
        _regex_url = r'^https:\/\/(youtu.be|www.youtube.com|music.youtube.com|soundcloud.com)\/\S+$'
        # no keyword 
        if len(args) == 0:
            return None
        # keyword is link for youtube, youtube music or soundcloud
        if re.match(_regex_url, args[0]):
            return args[0]
        # mutliple keywords -> will be used for youtube query
        else:
            return LinkProcessing.relevantLink(args)


if __name__ == "__main__":
    lp = LinkProcessing()
    output = lp.process(['ěš+č', '33'])
    print(output)

