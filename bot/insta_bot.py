from instabot import Bot

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = Bot()

    def login(self):
        self.bot.login(username=self.username, password=self.password)

    def logout(self):
        self.bot.logout()

    def send_message_to_large_accounts(self, message, hashtags, photo_path=None, video_path=None):
        for hashtag in hashtags:
            users = self.bot.get_hashtag_users(hashtag)
            for user in users:
                user_info = self.bot.get_user_info(user)
                if user_info['follower_count'] > 5000:
                    if photo_path:
                        self.bot.upload_photo(photo_path)
                    if video_path:
                        self.bot.upload_video(video_path)
                    self.bot.send_message(message, [user])

    def like_posts(self, hashtags, amount=10):
        for hashtag in hashtags:
            posts = self.bot.get_hashtag_medias(hashtag)
            for post in posts[:amount]:
                self.bot.like(post)

    def follow_users(self, hashtags, amount=10):
        for hashtag in hashtags:
            users = self.bot.get_hashtag_users(hashtag)
            for user in users[:amount]:
                self.bot.follow(user)

    def comment_on_posts(self, hashtags, comment, amount=10):
        for hashtag in hashtags:
            posts = self.bot.get_hashtag_medias(hashtag)
            for post in posts[:amount]:
                self.bot.comment(post, comment)