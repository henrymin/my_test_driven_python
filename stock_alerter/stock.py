import collections
import bisect
from enum import Enum

from .timeseries import TimeSeries
from .moving_average import MovingAverage

PriceEvent = collections.namedtuple("PriceEvent", ["timestamp", "price"])


class StockSignal(Enum):
    buy = 1
    neutral = 0
    sell = -1


class Stock(object):
    LONG_TERM_TIMESPAN = 10
    SHORT_TERM_TIMESPAN = 5

    def __init__(self, symbol):
        self.symbol = symbol
        self.history = TimeSeries()

    def update(self, timestamp, price):
        if price < 0:
            raise ValueError("price should not be negative")
        bisect.insort_left(self.price_history, PriceEvent(timestamp, price))

    @property
    def price(self):
        try:
            return self.history[-1].value
        except IndexError:
            return None

    def is_increasing_trend(self):
        return self.history[-3].value < \
               self.history[-2].value < self.history[-1].value

    def get_corssover_signal(self, on_date):
        NUM_DAYS = self.LONG_TERM_TIMESPAN + 1

        closing_price_list = \
            self.history.get_closing_price_list(on_date, NUM_DAYS)

        if len(closing_price_list) < 11:
            return StockSignal.neutral

        long_term_series = closing_price_list[-self.LONG_TERM_TIMESPAN:]
        prev_long_term_series = \
            closing_price_list[-self.LONG_TERM_TIMESPAN-1:-1]
        short_term_series = closing_price_list[-self.SHORT_TERM_TIMESPAN:]
        prev_short_term_series = \
            closing_price_list[-self.SHORT_TERM_TIMESPAN-1:-1]

        long_term_ma = MovingAverage.calc_ma(long_term_series, self.LONG_TERM_TIMESPAN)
        prev_long_term_ma = MovingAverage.calc_ma(prev_long_term_series, self.LONG_TERM_TIMESPAN)
        short_term_ma = MovingAverage.calc_ma(short_term_series, self.SHORT_TERM_TIMESPAN)
        prev_short_term_ma = MovingAverage.calc_ma(prev_short_term_series, self.SHORT_TERM_TIMESPAN)

        # BUY signal
        if self._is_short_term_below_to_above(prev_short_term_ma,
                                              prev_long_term_ma,
                                              short_term_ma,
                                              long_term_ma):
            return StockSignal.buy

        # SELL signal
        if self._is_short_term_below_to_above(prev_short_term_ma,
                                              prev_long_term_ma,
                                              short_term_ma,
                                              long_term_ma):
            return StockSignal.sell

        return StockSignal.neutral

    @staticmethod
    def _is_short_term_below_to_above(prev_ma, prev_reference_ma,
                                      current_ma, current_reference_ma):
        return prev_ma > prev_reference_ma \
            and current_ma < current_reference_ma
