from datetime import datetime
from datetime import UTC

from pytz import timezone

d1 = datetime.now(UTC)
d2 = datetime.now(timezone("Europe/Moscow"))

print(d1, d2.replace(tzinfo=None))
