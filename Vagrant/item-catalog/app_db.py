''' This module holds most of the items related to company and item data
 and the related sqlite user database '''

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Company(Base):

    ''' This class is used to hold company information in
     and sqlite database and is used with sqlalchemy '''
    __tablename__ = 'company'
    # columns
    name = Column(String(80), nullable=False)
    siteuri = Column(String(500), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        # Returns company data in easily serializable format
        return {
            'id': self.id,
            'name': self.name,
            'siteuri': self.siteuri
        }


class SalesItem(Base):

    ''' This class is used to hold item information in
     and sqlite database and is used with sqlalchemy '''
    __tablename__ = 'sales_item'
    # columns
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    price = Column(String(8))
    imageuri = Column(String(500))
    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship(Company)

    @property
    def serialize(self):
        # Returns item data in easily serializable format
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'imageuri': self.imageuri,
        }


# set up the catalog databse engine
engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
