class MovingAverage(object):
    @staticmethod
    def calc_ma(self, series, timespan):
        return sum([update.value for update in self.series]) \
               / self.timespan
