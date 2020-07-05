class ValuesQuerystring:
    def __init__(self, url):
        """
        Instantiates ValuesQuerystring which stores all values of a query string as class attributes.

        :param url: Url from which the values should be taken.
        """
        self.url = url
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
