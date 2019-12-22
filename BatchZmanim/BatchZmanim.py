from datetime import datetime, timedelta

from zmanim.zmanim_calendar import ZmanimCalendar
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar


class ZmanimDateList:
    """
    Accepts a list of JewishCalendar() objects.
    Initiates ZmanimCalendar() objects and allows you to call for zmanim times against the group.
    """

    zmanim_calendars = []
    zmanim_dict = {}
    all_zmanim = [
        'elevation_adjusted_sunrise',
        'elevation_adjusted_sunset',
        'hanetz',
        'shkia',
        'tzais',
        'tzais_72',
        'alos',
        'alos_72',
        'chatzos',
        'candle_lighting',
        # 'sof_zman_shma',
        'sof_zman_shma_gra',
        'sof_zman_shma_mga',
        # 'sof_zman_tfila',
        'sof_zman_tfila_gra',
        'sof_zman_tfila_mga',
        'mincha_gedola',
        'mincha_ketana',
        'plag_hamincha',
        # 'shaah_zmanis',
        'shaah_zmanis_gra',
        'shaah_zmanis_mga',
        # 'shaah_zmanis_by_degrees_and_offset',
        # 'is_assur_bemelacha',
    ]

    def __init__(self, date_list, candle_lighting_offset=None, *args, **kwargs):
        self.date_list = date_list
        self._init_zmanim_calendar(
            candle_lighting_offset=candle_lighting_offset, *args, **kwargs
        )

    def _init_zmanim_calendar(self, candle_lighting_offset=None, *args, **kwargs):
        """Initiate ZmanimCalendar() objects"""
        for date in self.date_list:
            self.zmanim_calendars.append(
                ZmanimCalendar(
                    date=date.gregorian_date,
                    candle_lighting_offset=candle_lighting_offset,
                    *args,
                    **kwargs,
                )
            )

    def get_zmanim(self, zmanim=None):
        """Helper function to get zmanim. Accepts """
        zmanim = zmanim if zmanim is not None else self.all_zmanim
        zmanim = zmanim if isinstance(zmanim, list) else list(zmanim)
        for date in self.zmanim_calendars:
            for zman in zmanim:
                if self.is_useful_zman(zman, date):
                    zman_datetime = getattr(date, zman, lambda: None)()
                    if date not in self.zmanim_dict.keys():
                        self.zmanim_dict.update({date: {}})
                    if zman not in self.zmanim_dict[date].keys():
                        self.zmanim_dict[date].update({zman: ""})
                    self.zmanim_dict[date][zman] = zman_datetime
        return self.zmanim_dict

    def is_useful_zman(self, zman, date):
        return True
        # if zman == "candle_lighting":
        #     print(type(date))
        #     if date.has_candle_lighting():
        #         return True


class JewishDateRange:
    """Creates a list of hebrew dates"""

    start_date = None
    jewish_days = []
    end_date = None
    significant_days_values = [e.name for e in JewishCalendar.SIGNIFICANT_DAYS]
    significant_days_check = [
        "assur_bemelacha",
        "tomorrow_assur_bemelacha",
        "candle_lighting",
        "delayed_candle_lighting",
        "yom_tov",
        "yom_tov_assur_bemelacha",
        "erev_yom_tov",
        "yom_tov_sheni",
        "erev_yom_tov_sheni",
        "chol_hamoed",
        "taanis",
        "rosh_chodesh",
        "erev_rosh_chodesh",
        "chanukah",
    ]
    special_has_methods = ["candle_lighting", "delayed_candle_lighting"]

    def __init__(self, end_date, start_date=datetime.now()):
        self.start_date = start_date
        self.end_date = end_date
        self.significant_days_all = (
            self.significant_days_check + self.significant_days_values
        )

        self._set_jewish_days()

    def _set_jewish_days(self):
        """Loop from start_day until end_date, initiating JewishDate() objects"""
        date = self.start_date
        for _ in range((self.end_date - self.start_date).days + 1):
            hebrew_day = JewishCalendar(date)
            self.jewish_days.append(hebrew_day)
            date += timedelta(days=1)

    def get_dates(self, filters=None, reverse=False):
        """Get date objects back as list, with optional filtering"""
        if filters:
            filters = filters if isinstance(filters, list) else list(filters)
            significant_days = self.get_significant_days(filters)
            significant_days = list(
                significant_days.values()
            )  # get values as list of lists
            significant_days = [
                y for x in significant_days for y in x
            ]  # reduce to one list
            # significant_days = list(dict.fromkeys(significant_days))  # de-dupe
            if not reverse:
                return_dates = significant_days
            else:
                return_dates = [
                    d for d in self.jewish_days if d not in significant_days
                ]
        else:
            return_dates = self.jewish_days
        return return_dates

    def get_significant_days(self, significant_days=None):
        """Returns a dictionary of JewishCalendar objects organized by significant start_date keys"""
        # TODO Add custom significant days, such as 'shabbos'
        significant_days = (
            significant_days
            if significant_days is not None
            else self.significant_days_all
        )
        significant_days_other = [
            s for s in significant_days if s not in self.significant_days_values
        ]

        day_dict = {}
        for day in self.jewish_days:
            # Find significant days using the JewishCalendar.significant_day() method
            significant_day = day.significant_day()
            if significant_day in significant_days:
                # TODO find a better way to check if keys are present
                if significant_day not in day_dict.keys():
                    day_dict.update({significant_day: []})
                day_dict[significant_day].append(day)

            # Find significant days using is_ and has_ methods from JewishCalendar()
            for significant_day in significant_days_other:
                method = (
                    "has_"
                    if significant_day in self.special_has_methods
                    else "is_" + significant_day
                )
                is_significant_day = getattr(day, method, lambda: None)()
                if is_significant_day:
                    # TODO find a better way to check if keys are present
                    if significant_day not in day_dict.keys():
                        day_dict.update({significant_day: []})
                    day_dict[significant_day].append(day)

        return day_dict

    def __repr__(self):
        return repr(
            f"JewishDateRange(end_date={self.end_date}, start_date={self.start_date})"
        )
