from datetime import datetime, timedelta
UTC_TZ = u'+00:00'

class Date:
    def __init__(self):
        super()

    @property
    def utc_offset(self):
        return timedelta(seconds=self.location['timezone']['offset'] / 1000)


    def add_new(self):

            st = "2020-05-20 10:00:00"
            et = "2020-05-20 10:00:00"
            if st and et:
                st = st[0] - self.utc_offset
                et = et[0] - self.utc_offset

    def main(self):
