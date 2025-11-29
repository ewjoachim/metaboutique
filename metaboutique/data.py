import asyncio
import dataclasses
import datetime
import io
import logging
import os
from collections.abc import Iterable
from typing import Any

from atproto_client import AsyncClient, Session, SessionEvent, models


@dataclasses.dataclass
class ShopLink:
    curator_comment: str | None
    url: str
    preview_url: str | None
    post_image_urls: list[str] | None
    author_comment: str | None
    author_handle: str
    author_profile_picture_url: str | None
    posted_at: datetime.datetime


async def fetch_shop_links():
    client = await init_client()

    # For this script to work immediately, paste a valid AT URI below:
    TARGET_POST_URI = (
        "at://sandrine2loffre.bsky.social/app.bsky.feed.post/3m67yhe4uac2l"
    )

    return await get_shop_links(client=client, at_uri=TARGET_POST_URI)


async def save_session(session_string: str) -> None:
    # Ensure the value cannot be shown in the logs
    print(f"::add-mask::{session_string}")
    # Then call the subprocess to set the secret
    await asyncio.create_subprocess_exec(
        "gh",
        "secret",
        "set",
        "BLUESKY_SESSION_STRING",
        stdin=io.StringIO(session_string),
    )


async def on_session_change(event: SessionEvent, session: Session) -> None:
    print("Session changed:", event, repr(session))
    if event in (SessionEvent.CREATE, SessionEvent.REFRESH):
        print("Saving changed session")
        await save_session(session.export())


async def init_client() -> AsyncClient:
    client = AsyncClient()
    client.on_session_change(on_session_change)

    if session_string := os.environ.get("BLUESKY_SESSION_STRING"):
        await client.login(session_string=session_string)
    else:
        await client.login(
            login=os.environ["BLUESKY_USERNAME"],
            password=os.environ["BLUESKY_PASSWORD"],
            auth_factor_token=os.environ["BLUESKY_AUTH_FACTOR_TOKEN"],
        )

    return client


class TreadNotFound(Exception):
    pass


class IgnorePost(Exception):
    pass


async def get_shop_links(client: AsyncClient, at_uri: str) -> Iterable[ShopLink]:
    retry_thread = True
    tasks: dict[asyncio.Task[Any], models.AppBskyFeedDefs.PostView] = {}

    while retry_thread:
        print("New thread ")
        response = client.get_post_thread(uri=at_uri, depth=1000, parent_height=0)
        retry_thread = False
        thread = response.thread
        if thread.py_type != "app.bsky.feed.defs#threadViewPost":
            raise TreadNotFound(str(thread))

        # Sort replies optionally (e.g., by time), currently API returns them usually sorted
        for reply in thread.replies or []:
            if not isinstance(reply, models.AppBskyFeedDefs.ThreadViewPost):
                continue
            if reply.post.author.handle != "sandrine2loffre.bsky.social":
                continue
            at_uri = reply.post.uri
            retry_thread = True
            tasks[
                asyncio.create_task(get_shop_link(client=client, post=reply.post))
            ] = reply.post

    shop_links = []
    async for link_task in asyncio.as_completed(*tasks):
        try:
            await link_task
        except IgnorePost:
            continue
        except Exception:
            post = tasks[link_task]
            logging.exception(f"Error on link {post.uri}")
            continue
        shop_links.append(link)

    return shop_links


async def get_shop_link(
    client: AsyncClient, post: models.AppBskyFeedDefs.PostView
) -> ShopLink:
    assert post.record
    if len(post.record.facets) != 1 or len(post.record.facets[0].features) != 1:
        raise IgnorePost

    embed = post.embed

    return ShopLink(
        curator_comment="",
        url=post.record.facets[0].features[0].uri,
        preview_url="",
        post_image_urls="",
        author_comment="",
        author_handle="",
        author_profile_picture_url="",
        posted_at="",
    )
