from random import shuffle

from fire import Fire
from tqdm import tqdm

from nogi import engine, metadata
from nogi.db.nogi_blog_content import NogiBlogContent
from nogi.db.nogi_blog_summary import NogiBlogSummary
from nogi.db.nogi_members import NogiMembers
from nogi.utils.post_extractor import PostExecutor
from nogi.utils.updater import Updater
from nogi.storages.gcs import GCS


class CommandLine:

    def __init__(self) -> None:

        # Blog
        self.blog_content = NogiBlogContent(engine, metadata, role='writer')
        self.blog_summary = NogiBlogSummary(engine, metadata, role='writer')
        self.blog_member = NogiMembers(engine, metadata)

        # GCS
        self.gcs = GCS()

    def crawl(self, bucket: str = 'nogi-test'):
        _members = self.blog_member.get_current_members()
        shuffle(_members)
        for member in tqdm(_members):
            Updater(member=member, blog_db=self.blog_summary).run()
            PostExecutor(
                member=member,
                summary_db=self.blog_summary,
                content_db=self.blog_content,
                gcs_client=self.gcs,
                bucket=bucket
            ).run()


if __name__ == "__main__":
    Fire(CommandLine)
