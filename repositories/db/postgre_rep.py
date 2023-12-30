from peewee import PostgresqlDatabase
from data import configuration

db = PostgresqlDatabase(configuration.database_connection_parameters.database,
                        user=configuration.database_connection_parameters.user,
                        password=configuration.database_connection_parameters.password,
                        host=configuration.database_connection_parameters.host,
                        port=configuration.database_connection_parameters.port)
