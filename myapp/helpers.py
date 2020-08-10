import datetime

import myapp.database_handlers as db_handlers


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


class RepresentationGame:
    def __init__(self, hometeam, guestteam):
        game = db_handlers.query_gamedates(hometeam, guestteam)

        self.date = game.date
        self.time = game.time
        self.gruppe = 'None'
        self.untergruppe = game.date.month
        self.heim = game.home_team.name
        self.gast = game.guest_team.name
        self.ort = game.pool

    def __str__(self):
        return f'{self.date.strftime("%d.%m.%y")},{self.time.strftime("%H.%M")},{self.gruppe},{str(self.untergruppe)},' \
               f'{self.heim},{self.gast},{self.ort}'

    def __repr__(self):
        return self.__str__()


class Schedule:
    def __init__(self, league_id):
        self.all_games = []

        teams = db_handlers.query_teams(league_id=league_id)

        for hometeam in teams:
            for guestteam in [team for team in teams if team != hometeam]:
                repr_game = RepresentationGame(hometeam, guestteam)
                self.all_games.append(repr_game)

    def __repr__(self):
        return str([game for game in self.all_games])
