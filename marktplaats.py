from typing import Any, Dict, List, Set, Union
from contextlib import contextmanager
from pathlib import Path
import httpx
import telegram
import config

URL = 'https://www.marktplaats.nl/lrp/api/search'
Item = Dict[str, Any]
bot = telegram.Bot(token=config.token)


def get_items(game: str) -> List[Item]:
    query: Dict[str, Union[str, int]] = dict(
        l1CategoryId=1099,
        l2CategoryId=1233,
        limit=30,
        offset=0,
        query=game,
        searchInTitleAndDescription="true",
        viewOptions="list-view",
    )
    resp = httpx.get(URL, params=query)
    resp.raise_for_status()
    return resp.json()['listings']


def format_item(item: Item) -> str:
    price = item['priceInfo'].get('priceCents', 0) / 100
    lines = [
        item['title'],
        str(price) + ' ' + item['priceInfo'].get('priceType', ''),
        item['date'],
        item['location'].get('cityName', ''),
        'https://www.marktplaats.nl' + item['vipUrl'],
    ]
    return '\n'.join(lines)


@contextmanager
def cache_manager():
    path = Path('.ids.txt')
    ids: Set[str] = set()
    if path.exists():
        ids = set(path.read_text().split())
    yield ids
    path.write_text('\n'.join(ids))


def notify(text: str) -> None:
    for chat_id in config.chat_ids:
        bot.send_message(chat_id=chat_id, text=text)
    print(text)


def main() -> None:
    with cache_manager() as cache_ids:
        first_run = not cache_ids
        for game in config.games:
            for item in get_items(game):
                iid = item['itemId'].strip()
                if iid in cache_ids:
                    continue
                cache_ids.add(iid)
                if first_run:
                    continue
                text = format_item(item)
                notify(text)


if __name__ == '__main__':
    main()
