"""
Module dates.py
"""
import datetime
import logging

import pandas as pd

import config


class Dates:
    """
    Notes
    -----

    Determines the calculation dates.
    """

    def __init__(self):
        """
        The constructor.
        """

        self.__configurations = config.Config()

        # logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self) -> list[str]:

        ends = datetime.datetime.strptime(__date_string=self.__configurations.ending, __format='%Y-%m-%d')

        if self.__configurations.starting:
            starts = datetime.datetime.strptime(__date_string=self.__configurations.starting, __format='%Y-%m-%d')
            values = pd.date_range(start=starts, end=ends, freq='MS').to_list()
            datestr_ = [str(value.date()) for value in values]
        else:
            datestr_ = [str(ends.replace(day=1).date())]

        self.__logger.info('Dates\n%s', datestr_)

        return datestr_
