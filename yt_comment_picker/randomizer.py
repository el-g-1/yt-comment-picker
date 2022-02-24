import random


class Randomizer:
    def __init__(self, comments, remove_duplicate_users=False, specific_text=None):
        self.comments = comments
        self.remove_duplicate_users = remove_duplicate_users
        self.specific_text = specific_text

    def randomize(self):
        filtered_comments = self._filter()
        if not filtered_comments:
            return None
        return random.choice(filtered_comments)

    def _filter(self):
        def is_comment_valid(comm):
            if self.specific_text:
                if self.specific_text.lower() not in comm.text.lower():
                    return False
            if self.remove_duplicate_users:
                if comm.author.link in author_links:
                    return False
            return True

        filtered_comments = []
        author_links = set()
        for comment in self.comments:
            if is_comment_valid(comment):
                author_links.add(comment.author.link)
                filtered_comments.append(comment)
        return filtered_comments
