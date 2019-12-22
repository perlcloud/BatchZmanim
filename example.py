from datetime import datetime, timedelta

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar

from BatchZmanim import JewishDateRange, ZmanimDateList

location = GeoLocation('Lakewood, NJ', 40.0721087, -74.2400243, 'America/New_York', elevation=15)
start_date = datetime(2019, 12, 1)
end_date = datetime(2020, 1, 30)
special_days = [
    'chanukah',
]
zmanim = [
    'candle_lighting',
    'mincha_ketana',
    'mincha_gedola'
]

date_range = JewishDateRange(end_date, start_date=start_date)
date_list = date_range.get_dates(filters=special_days)
date_zmanim = ZmanimDateList(date_list, geo_location=location)
zmanim_datetimes = date_zmanim.get_zmanim(zmanim)

for k, v in zmanim_datetimes.items():
    print(k.date.strftime('Date: %d, %b %Y'))
    for key, value in v.items():
        print('\t', key + ':', value)
