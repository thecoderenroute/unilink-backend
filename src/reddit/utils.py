from fastapi import File, UploadFile
import yaml
import tweepy
import praw
from src.reddit.settings import Settings
from src.reddit.models import Submission, Redditor
from pprint import pprint


class RedditWrapper:
    def __init__(self):
        self.settings = Settings()
        # self.reddit = praw.Reddit(
        #     client_id=self.settings.client_id,
        #     client_secret=self.settings.client_secret,
        #     # password=self.settings.password,
        #     user_agent=self.settings.user_agent,
        #     username=self.settings.username,
        # )
        self.reddit = praw.Reddit(
            client_id=self.settings.client_id,
            client_secret=self.settings.client_secret,
            redirect_uri="unilink://reddit.login",
            user_agent="unilink",
        )
        self.refresh_token = ""
        pass

    def autthorise_user(self, code):
        res = self.reddit.auth.authorize(code)
        # print(res)
        print(f"reddit me: {self.reddit.user.me()}")
        return res

    def create_instance_using_refresh_token(self, refresh_token, access_token):
        self.reddit = praw.Reddit(
            client_id=self.settings.client_id,
            client_secret=self.settings.client_secret,
            refresh_token=refresh_token,
            # access_token=access_token,
            # redirect_uri="unilink://reddit.login",
            user_agent="unilink",
        )
        self.refresh_token = refresh_token
        print(f"scopes: {self.reddit.auth.scopes()}")
        print(self.reddit.user.me())
        return self.reddit.user.me()

    def map_submission(self, submission):
        mapped_submission = Submission(
            submission.author,
            submission.author_flair_text,
            submission.clicked,
            submission.comments,
            submission.created_utc,
            submission.distinguished,
            submission.edited,
            submission.id,
            submission.is_original_content,
            submission.is_self,
            submission.link_flair_text,
            submission.locked,
            submission.name,
            submission.num_comments,
            submission.over_18,
            submission.saved,
            submission.score,
            submission.selftext,
            submission.spoiler,
            submission.stickied,
            submission.subreddit,
            submission.title,
            submission.upvote_ratio,
            submission.url,
        )
        return mapped_submission

    def map_redditor(self, redditor_object):
        submissions = redditor_object.submissions.new()
        l = []
        for i in submissions:
            l.append(self.map_submission(i))
        mapped_redditor = Redditor(
            redditor_object.comment_karma,
            redditor_object.comments,
            l,
            redditor_object.created_utc,
            redditor_object.has_verified_email,
            redditor_object.icon_img,
            redditor_object.id,
            redditor_object.is_employee,
            redditor_object.is_friend,
            redditor_object.is_mod,
            redditor_object.is_gold,
            redditor_object.link_karma,
            redditor_object.name,
            redditor_object.subreddit,
        )
        return mapped_redditor

    def get_new_post(self, rslash):
        subreddit = self.reddit.subreddit(rslash)
        for submission in subreddit.new(limit=1):
            mapped_submission = self.map_submission(submission)
            return mapped_submission

    def get_hot_post(self, rslash):
        subreddit = self.reddit.subreddit(rslash)
        print(subreddit.title)
        c = 0
        for submission in subreddit.hot(limit=2):
            if c == 0:
                c += 1
                continue
            mapped_submission = self.map_submission(submission)
            return mapped_submission

    def get_top_post(self, rslash):
        subreddit = self.reddit.subreddit(rslash)
        print(subreddit.title)
        for submission in subreddit.top(limit=1):
            print(f"submission: {submission}")
            mapped_submission = self.map_submission(submission)
            print(f"mapped_submission {mapped_submission}")
            return mapped_submission

    def get_redditor_by_username(self, redditor_name="RagingBox08"):
        redditor_object = self.reddit.redditor(redditor_name)
        # print(f'redditor_object : {redditor_object}')
        # print(f'submissions: {redditor_object.submissions.hot()}')
        # for i in redditor_object.submissions.hot():
        #     print(f'i:{type(i)}')
        mapped = self.map_redditor(redditor_object).__dict__
        submissions = mapped["submissions"]
        l = []
        for i in submissions:
            mapped_sub = self.map_submission(i).__dict__
            l.append(mapped_sub)
        mapped["submissions"] = l
        return mapped

    def get_user_subreddits(
        self,
    ):
        if self.refresh_token != "":
            # reddit = praw.Reddit(
            #     client_id=self.settings.client_id,
            #     client_secret=self.settings.client_secret,
            #     refresh_token=self.refresh_token,
            #     user_agent="unilink",
            # )
            # self.reddit = praw.Reddit(
            #     client_id=self.settings.client_id,
            #     client_secret=self.settings.client_secret,
            #     refresh_token=self.refresh_token,
            #     # access_token=access_token,
            #     # redirect_uri="unilink://reddit.login",
            #     user_agent="unilink",
            # )
            print("get_user_subreddit called")
            subs = self.reddit.user.subreddits()
            for i in subs:
                print(i.display_name)
            return "get_user_sub called"
        else:
            return "Not logged in to reddit"

    def post_on_subreddit(self, subreddit_name, text, title):
        print("post on subreddit")
        try:
            sub = self.reddit.subreddit(subreddit_name)
            print(sub)
            res = sub.submit(title=title, selftext=text)
            print(res)
            return res
        except Exception as e:
            print(e)
            return str(e)

    def post_image_on_subreddit(
        self, subname: str, my_file: UploadFile = File(...), title: str = ""
    ):
        try:
            sub = self.reddit.subreddit(subname)
            print(sub)
            res = sub.submit_image(title=title, image=my_file)
            print(res)
            return res
        except Exception as e:
            print(e)
            return str(e)
