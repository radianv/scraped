# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from models import Booking, db_connect, create_booking_table, drop_booking_table

class BookingPipeline(object):
    """Despegar pipeline for storing scraped items in the database"""
    def __init__(self):
        """Initializes database connection and sessionmaker.
           Creates deals table.
        """
        engine = db_connect()
        drop_booking_table(engine)
        create_booking_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()
        deal = Booking(**item)

        try:
            session.add(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
