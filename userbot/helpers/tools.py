from html_telegraph_poster import TelegraphPoster


def media_type(message):
    if message and message.photo:
        return "كتابة"
    if message and message.audio:
        return "اغنية"
    if message and message.voice:
        return "صوتي"
    if message and message.video_note:
        return "جولة"
    if message and message.gif:
        return "متحركة"
    if message and message.sticker:
        return "ملصق"
    if message and message.video:
        return "فيديو"
    if message and message.document:
        return "ملف"
    return None


async def post_to_telegraph(page_title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "CatUserbot"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=page_title,
        author=auth_name,
        author_url="https://t.me/Jmthon",
        text=html_format_content,
    )
    return post_page["url"]
