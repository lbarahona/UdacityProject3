from app_db import Base, Company, SalesItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)()


def all_companies_db():
    ''' return all companies in the DB '''
    return DBSession.query(Company).all()


def get_company_from_id_db(company_id):
    ''' return a specific company from the DB based on it's id '''
    return DBSession.query(Company).filter_by(id=company_id).one()


def add_company_db(name, site_uri):
    ''' add a company to the DB '''
    new_company = Company(name=name, siteuri=site_uri)
    DBSession.add(new_company)
    DBSession.commit()


def edit_company_db(company_id, name, site_uri):
    ''' edit an existing company in the DB '''
    target_company = get_company_from_id_db(company_id)
    if target_company != []:
        target_company.name = name
        target_company.siteuri = site_uri
        DBSession.commit()


def delete_company_db(company_id):
    ''' delete an existing company from the DB '''
    target_company = get_company_from_id_db(company_id)
    if target_company != []:
        delete_company_db
        delete_company_sales_items(company_id)
        DBSession.delete(target_company)
        DBSession.commit()


def delete_company_sales_items(company_id):
    ''' delete an item from a company in the DB '''
    DBSession.query(SalesItem).filter_by(company_id=company_id).delete()
    DBSession.commit()


def get_sales_items_from_id_db(company_id):
    ''' return all items for a company from the DB based on the company id '''
    items = DBSession.query(SalesItem).filter_by(company_id=company_id)
    return items


def get_sales_item_from_id_db(company_id, item_id):
    ''' get a specific sales item from the DB based on company/item ids '''
    # this has error handling.  Most of the application has it's error handling
    # TODO: add it to all the rest of the related functions here as well
    try:
        item = DBSession.query(SalesItem).filter_by(company_id=company_id,
                                                    id=item_id).one()
    except:
        item = None
    return item


def add_sales_item_db(name, price, image_uri, company_id):
    ''' add a sales item to a company in the DB '''
    new_item = SalesItem(name=name, price=price,
                         imageuri=image_uri, company_id=company_id)
    DBSession.add(new_item)
    DBSession.commit()


def edit_sales_item_db(company_id, item_id, name, price, image_uri):
    ''' edit an existing sales item in the DB '''
    target_item = get_sales_item_from_id_db(company_id, item_id)
    if target_item != []:
        target_item.name = name
        target_item.price = price
        target_item.imageuri = image_uri
        DBSession.commit()


def delete_sales_item_db(company_id, item_id):
    ''' delete an existing sales item from the DB '''
    target_item = get_sales_item_from_id_db(company_id, item_id)
    if target_item != []:
        DBSession.delete(target_item)
        DBSession.commit()


def empty_all_data():
    ''' this empties all data in the tables for the DB
    but keeps the tables intact '''
    DBSession.query(Company).delete()
    DBSession.query(SalesItem).delete()
