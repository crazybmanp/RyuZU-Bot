import datetime


def prune_respects(db):
    now = datetime.datetime.now()
    _all = db.all()
    d = []
    for a in _all:
        dt = datetime.datetime.strptime(a['timestamp'], '%b %d %Y %I:%M%p')
        if now - dt > datetime.timedelta(days=1):
            d.append(a.eid)
    db.remove(eids=d)
