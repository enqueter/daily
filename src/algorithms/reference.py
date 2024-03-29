"""
Module reference.py
"""
import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.unload

import config


class Reference:
    """

    Notes
    -----

    Each instance of the reference data frame describes the characteristics of a unique sequence of
    telemetric data.  The details include sequence identification code, the geographic coordinates of
    the telemetric device, the pollutant being measured, the unit of measure, etc.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()

        # S3 Unload Instance
        self.__unload = src.s3.unload.Unload(service=self.__service)

    def __read(self, filename: str) -> pd.DataFrame:
        """

        :param filename: the name of the Amazon S3 (Simple Storage Service) file being read.
        :return:
        """

        key_name = f'{self.__s3_parameters.path_internal_references}{filename}'
        buffer = self.__unload.exc(
            bucket_name=self.__s3_parameters.internal, key_name=key_name)

        try:
            return pd.read_csv(filepath_or_buffer=buffer, header=0, encoding='utf-8')
        except ImportError as err:
            raise err from err

    def __excerpt(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        # Extract the records in focus.
        excerpt = blob.copy().loc[blob['sequence_id'].isin(self.__configurations.sequence_id_filter), :]

        return excerpt

    def exc(self) -> pd.DataFrame:
        """

        :return:
          data : DataFrame
            An integration of (a) substances metadata, (b) stations gazetteer data,
            and (c) telemetric devices metadata, i.e., the registry.
        """

        # The frame of reference data
        frame = self.__read(filename='reference.csv')

        # Excerpt
        reference: pd.DataFrame = self.__excerpt(blob=frame)

        return reference
