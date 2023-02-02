
from apisls.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apisls.database.models import Base, Plant
from aws_xray_sdk.ext.sqlalchemy.query import XRaySessionMaker
from typing import List

trace_sql_query = True


def get_engine():
    connection_str = "mariadb+pymysql://***"
    engine = create_engine(connection_str)
    # from sqlalchemy_utils import database_exists, create_database
    #
    # if not database_exists(engine.url):
    #     logger.info("Creating database")
    #     create_database(engine.url)
    #
    # logger.info(f"Database exists: {database_exists(engine.url)}")
    return engine


def get_session():
    if trace_sql_query:
        Session = XRaySessionMaker(bind=get_engine())
        return Session()
    return sessionmaker(bind=get_engine())()


def init():

    logger.info("Initializing DB")
    engine = get_engine()
    Base.metadata.create_all(engine)


def create_plant(name: str):
    logger.info("Creating plant")
    session = get_session()
    plant = Plant(name=name)
    session.add(plant)
    session.commit()


def get_plant_list():
    session = get_session()

    plants = session.query().with_entities(Plant.id, Plant.name).all()
    return [{"id": id, "name": name} for id, name in plants]
