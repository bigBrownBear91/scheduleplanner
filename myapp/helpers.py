import datetime

class ValuesQuerystring:
    def __init__(self, url):
        """
        Instantiates ValuesQuerystring which stores all values of a query string as class attributes.

        :param url: Url from which the values should be taken.
        """
        self.url = url

        if self.url:
            self.extract_parameters()

    def extract_parameters(self):
        querystring = self.url.split('?')[1]
        arguments = querystring.split('&')
        for argument in arguments:
            arg = argument.split('=')
            try:
                arg[1] = int(arg[1])
            except ValueError:
                pass

            setattr(self, arg[0], arg[1])

    def __repr__(self):
        return '{}'.format(self.__dict__)


class StringToDate:
    def __init__(self, date):
        if not isinstance(date, str):
            raise TypeError('Input is not a string')

        self.date_as_string = date
        self.date_as_date = None

        if len(self.date_as_string.split('.')[-1]) < 4:
            self.date_as_date = datetime.datetime.strptime(self.date_as_string, '%d.%m.%y').date()
        if len(self.date_as_string.split('.')[-1]) >= 4:
            self.date_as_date = datetime.datetime.strptime(self.date_as_string, '%d.%m.%Y').date()


class StringToTime:
    def __init__(self, time):
        self.time_as_string = time
        self.time_as_time = None

        self.time_as_time = datetime.datetime.strptime(self.time_as_string, '%H.%M').time()
