# marktplaats

A little script to monitor [marktplaats.nl](https://www.marktplaats.nl/) for new board games and send notifications in Telegram. With a little tweaking (changing `l1CategoryId` and `l2CategoryId`) can be used to monitor other items.

1. `python3 -m pip install -r requirements.txt`
1. `cp config_example.py config.py`
1. Modify `config.py`
1. `python3 marktplaats.py`
