import yadisk
from data import configuration
from loguru import logger
import os

disk = yadisk.YaDisk(token=configuration.cloud_drive_token)
