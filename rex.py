import re
import unittest

def pathpart(s):
    parse = re.search(r'^/?([^/]*)/?(.*)', s)
    return parse.group(1), parse.group(2)


tail = 'abc/def//ghi'
while True:
    (f, tail) = pathpart(tail)
    print(f)
    if tail is None or tail == '':
        break

print()


class ParseTimeError(Exception):
    pass


#
#
#
def daysInMonth(year, month):

    DaysInMonth = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    if month != 2 or (year % 4) != 0:
        return DaysInMonth[month-1]

    # if we get here, it's February in a year divisible by 4
    # that's _usually_ a leap year, but there are exceptions!

    if (year % 100) != 0:
        return 29

    # if we get here, it's February in a year divisible by 100

    if (year % 400) == 0:
        # this is a year like 2000, which is divisible by 400, and hence a leap year
        return 29

    # this is a year like 2100, which would be a leap year, but is not because it's not divisible by 400
    return 28


def parsetime(s):
    match_date = r'^[\s]*(?P<year>[0-9]{2,4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})($|T|-| )(?P<time>.*)'
    parse_d = re.search(match_date, s)
    if parse_d is None:
        raise ParseTimeError("Invalid y-m-d")

    year_num = 0
    year = parse_d.group('year')
    if len(year) == 4:
        year_num = int(year)
    elif len(year) == 3:
        year_num = 1900 + int(year)
    elif len(year) == 2:
        year_num = 2000 + int(year)
    year = '%04d' % year_num

    month_num = int(parse_d.group('month'))
    if month_num not in range(1, 13):
        raise ParseTimeError("Month must be in range [1,12]")
    month = '%02d' % month_num

    days_in_this_month = daysInMonth(year_num, month_num)
    if int(parse_d.group('day')) not in range(1, days_in_this_month + 1):
        raise ParseTimeError(f'Day must be in range [1,%d]' % days_in_this_month)
    day = '%02d' % int(parse_d.group('day'))

    hour = '00'
    minute = '00'
    second = '00'
    if len(parse_d.group('time')) > 0:
        match_time = r'^(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{1,2})(($|:)(?P<second>[0-9]{1,2})?)?'
        parse_t = re.search(match_time, parse_d.group('time'))

        if parse_t is None:
            raise ParseTimeError()

        if int(parse_t.group('hour')) not in range(0, 24):
            raise ParseTimeError()
        hour = '%02d' % int(parse_t.group('hour'))

        if int(parse_t.group('minute')) not in range(0, 60):
            raise ParseTimeError()
        minute = '%02d' % int(parse_t.group('minute'))

        if parse_t.group(3) is not None and parse_t.group(3).startswith(':'):
            if parse_t.group('second') is None:
                raise ParseTimeError("Trailing M:S colon")
            if int(parse_t.group('second')) not in range(0, 60):
                raise ParseTimeError("Seconds out of range")
            else:
                second = '%02d' % int(parse_t.group('second'))

    return year, month, day, hour, minute, second


class TestParseTime(unittest.TestCase):

    @staticmethod
    def parse(time):
        (year, month, day, hour, minute, second) = parsetime(time)
        result = f'%s-%s-%sT%s:%s:%s' % (year, month, day, hour, minute, second)
        return result

    def testCorrectDates(self):
        self.assertEqual(self.parse('2017-09-17'), '2017-09-17T00:00:00')
        self.assertEqual(self.parse('2017-09-17T'), '2017-09-17T00:00:00')
        self.assertEqual(self.parse('2017-09-17-'), '2017-09-17T00:00:00')
        self.assertEqual(self.parse('2017-09-17 '), '2017-09-17T00:00:00')

        self.assertEqual(self.parse('2017-9-17'), '2017-09-17T00:00:00')
        self.assertEqual(self.parse('2017-09-7'), '2017-09-07T00:00:00')
        self.assertEqual(self.parse('2017-9-7'), '2017-09-07T00:00:00')
        self.assertEqual(self.parse('17-9-7'), '2017-09-07T00:00:00')
        self.assertEqual(self.parse('17-09-7'), '2017-09-07T00:00:00')
        self.assertEqual(self.parse('17-9-17'), '2017-09-17T00:00:00')
        self.assertEqual(self.parse('17-11-27'), '2017-11-27T00:00:00')
        self.assertEqual(self.parse('2017-02-28'), '2017-02-28T00:00:00')
        self.assertEqual(self.parse('2016-02-29'), '2016-02-29T00:00:00')   # 2016 is a leap year
        self.assertEqual(self.parse('2000-02-29'), '2000-02-29T00:00:00')   # 2000 is a leap year

    def testCorrectTimes(self):
        self.assertEqual(self.parse('2017-09-17T22:20:06'), '2017-09-17T22:20:06')
        self.assertEqual(self.parse('2017-09-17T22:2:06'), '2017-09-17T22:02:06')
        self.assertEqual(self.parse('2017-09-17T22:12:6'), '2017-09-17T22:12:06')
        self.assertEqual(self.parse('2017-09-17T22:4:1'), '2017-09-17T22:04:01')
        self.assertEqual(self.parse('2017-09-17T00:00:00'), '2017-09-17T00:00:00')
        self.assertEqual(self.parse('2017-09-17T23:45'), '2017-09-17T23:45:00')

    def testMissingMinute(self):
        # if there is a time, then there must be minutes
        self.assertRaises(ParseTimeError, parsetime, '2017-11-30T12')
        self.assertRaises(ParseTimeError, parsetime, '2017-11-30T12:')

    def testTrailingColon(self):
        # if there is a colon after the minutes field, then there must be some seconds.
        self.assertRaises(ParseTimeError, parsetime, '2017-09-17T12:34:')

    def testBadDateEnding(self):
        self.assertRaises(ParseTimeError, parsetime, '2017-09-17Q')

    def testBadMonth(self):
        self.assertRaises(ParseTimeError, parsetime, '2017-0-17')
        self.assertRaises(ParseTimeError, parsetime, '2017-13-17')
        self.assertRaises(ParseTimeError, parsetime, '2017-a3-17')
        self.assertRaises(ParseTimeError, parsetime, '2017-Sep-17')
        self.assertRaises(ParseTimeError, parsetime, '2017--09-17')
        self.assertRaises(ParseTimeError, parsetime, '2017--9-17')

    def testBadDay(self):
        self.assertRaises(ParseTimeError, parsetime, '2017-11-0')
        self.assertRaises(ParseTimeError, parsetime, '2017-11-00')  # 0 is not a valid day.
        self.assertRaises(ParseTimeError, parsetime, '2017-11-32')
        self.assertRaises(ParseTimeError, parsetime, '2017-11-31')  # november has only 30 days
        self.assertRaises(ParseTimeError, parsetime, '2017-2-29')   # february has only 28 days in 2017
        self.assertRaises(ParseTimeError, parsetime, '2017-11-aa')

        self.assertRaises(ParseTimeError, parsetime, '2017-04-31')  # april has only 30 days

        self.assertRaises(ParseTimeError, parsetime, '2017-02-29')  # 2017 is not a leap year
        self.assertRaises(ParseTimeError, parsetime, '2100-02-29')  # 2100 is NOT a leap year!

    def testBadHour(self):
        self.assertRaises(ParseTimeError, parsetime, '2017-09-17 24:00:00')
        self.assertRaises(ParseTimeError, parsetime, '2017-09-17 -4:00:00')

    def testBadMinute(self):
        self.assertRaises(ParseTimeError, parsetime, '2017-09-17-12:34:bb')
        self.assertRaises(ParseTimeError, parsetime, '2017-09-17-12:34:60')
        self.assertRaises(ParseTimeError, parsetime, '2017-09-17-12:34:-12')


class PhoneNumberError(Exception):
    pass


def parsephonenumber(s):

    parts = None
    if parts is None:
        # note the (?P=sep): that field must match the previous sep field.
        # xxx.xxx.xxxx and xxx-xxx-xxxx are valid, but xxx.xxx-xxxx and xxx-xxx.xxxx are not valid.
        parts = re.search(r'^([01]\+)?(?P<ac>[1-9][0-9]{2})(?P<sep>[-.])(?P<prefix>[1-9][0-9]{2})(?P=sep)(?P<line>[0-9]{4})(?P<ext>.*)?', s)
    if parts is None:
        parts = re.search(r'^(?P<ac>)(?P<prefix>[1-9][0-9]{2})[-.](?P<line>[0-9]{4})(?P<ext>.*)?', s)
    if parts is None:
        raise PhoneNumberError()

    extension = None
    if len(parts.group('ext')) > 0:
        parse_ex = re.search(r'^\s*(ext|x)?\s*(?P<ext>[0-9]+)', parts.group('ext'))
        if parse_ex is not None:
            extension = parse_ex.group('ext')

    return parts.group('ac'), parts.group('prefix'), parts.group('line'), (('ex:' + extension) if extension else '')


class TestPhoneNumber(unittest.TestCase):

    @staticmethod
    def parse(phone):
        (ac, pre, line, ext) = parsephonenumber(phone)
        result = f'%s %s %s %s' % (ac, pre, line, ext)
        return result

    def testWithAreaCode(self):
        self.assertEqual(self.parse('206-465-6421'), '206 465 6421 ')
        self.assertEqual(self.parse('206.465.6421'), '206 465 6421 ')
        self.assertRaises(PhoneNumberError, parsephonenumber, '206-465.6421')
        self.assertRaises(PhoneNumberError, parsephonenumber, '206.465-6421')
        self.assertRaises(PhoneNumberError, parsephonenumber, '006.465.6421')
        self.assertRaises(PhoneNumberError, parsephonenumber, '006-465-6421')
        self.assertRaises(PhoneNumberError, parsephonenumber, '206-065-6421')
        self.assertRaises(PhoneNumberError, parsephonenumber, '20-465-6421')

    def testWithoutAreaCode(self):
        self.assertEqual(self.parse('465-6421'), ' 465 6421 ')
        self.assertEqual(self.parse('465.6421'), ' 465 6421 ')
        self.assertRaises(PhoneNumberError, parsephonenumber, '465-642')
        self.assertRaises(PhoneNumberError, parsephonenumber, '4465-642')

    def testWithExtension(self):
        self.assertEqual(self.parse('465-6421x44'), ' 465 6421 ex:44')

    def testWithAreaCodeAndExtension(self):
        self.assertEqual(self.parse('0+206-465-6421     ext 33'), '206 465 6421 ex:33')
        self.assertEqual(self.parse('206-465-6421 104'), '206 465 6421 ex:104')


if __name__ == '__main__':
    unittest.main()
