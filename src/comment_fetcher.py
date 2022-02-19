import googleapiclient.discovery
from comment import Comment, Author


class Fetcher:
    def __init__(self, developer_key, video_id, part_snippet):
        self.video_id = video_id
        self.developer_key = developer_key
        self.part_snippet = part_snippet

    def _make_comment_link(self, comment_id):
        return "https://www.youtube.com/watch?v=" + self.video_id + "+&lc=" + comment_id

    def parsed(self, items):
        local_comments = []
        for comment in items:
            comment_author = Author(
                name=comment["snippet"]["topLevelComment"]["snippet"][
                    "authorDisplayName"
                ],
                link=comment["snippet"]["topLevelComment"]["snippet"][
                    "authorChannelUrl"
                ],
                pic_link=comment["snippet"]["topLevelComment"]["snippet"][
                    "authorProfileImageUrl"
                ],
            )
            comment_complete = Comment(
                comment_author,
                link=self._make_comment_link(comment["id"]),
                text=comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                date=comment["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
            )
            local_comments.append(comment_complete)
        return local_comments

    def fetch(self):
        youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=self.developer_key
        )

        request = youtube.commentThreads().list(
            part=self.part_snippet, videoId=self.video_id, maxResults=100
        )
        response = request.execute()
        all_comments = self.parsed(response["items"])

        while "nextPageToken" in response:
            next_page = response["nextPageToken"]
            request = youtube.commentThreads().list(
                pageToken=next_page,
                part=self.part_snippet,
                videoId=self.video_id,
                maxResults=100,
            )
            response = request.execute()
            all_comments += self.parsed(response["items"])
        return all_comments


# with open('/Users/kisa/PycharmProjects/CommentPicker/data/yt_api_key.txt') as file:
#     api_key = file.read()
# test_1 = Fetcher(api_key, 'J3giFe91HAs', 'snippet')
# all_comments = test_1.fetch()
# print(len(all_comments))
# for comment in all_comments:
#     print(comment)

# if __name__ == "__main__":
#     main()
