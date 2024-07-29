from datetime import datetime
import pytz
import time

def get_dt_now():
    """
    RETURNS CURRENT DATE-TIME IN PHILIPPINE TIMEZONE
    """
    utc_now = pytz.utc.localize(datetime.utcnow())
    return utc_now.astimezone(pytz.timezone('Asia/Manila'))