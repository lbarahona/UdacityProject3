''' This file is used when setting up the database for the first time or
 resetting data to the default sample data '''
 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app_db import Company, Base, SalesItem


def load_default_data(session):
    ''' This loads in all the default data given an sqlalchemy
    session as an argument '''

    #Nintendo
    company_1 = Company(
        name="Nintendo", siteuri="http://www.nintendo.com/")
    session.add(company_1)

    sales_item_0 = SalesItem(
        name="Mario Bros",
        imageuri=("http://upload.wikimedia.org/wikipedia/en/0/03/Super_Mario_Bros._box.png"),
        price="$40.00", company=company_1)
    session.add(sales_item_0)

    sales_item_1 = SalesItem(
        name="The Legend Of Zelda",
        imageuri=("http://www.gamerbolt.com/wp-content/uploads/2014/11/The-Legend-of-Zelda-Ocarina-of-Time-Collectors-Edition.jpg"),
        price="$45.00", company=company_1)
    session.add(sales_item_1)

    sales_item_2 = SalesItem(
        name="Donkey Kong",
        imageuri=("http://vgboxart.com/boxes/CD-I/46372-donkey-kong.png"),
        price="$30.00", company=company_1)
    session.add(sales_item_2)

    sales_item_3 = SalesItem(
        name="Balloon Fight",
        imageuri=("http://img.gamefaqs.net/box/7/9/7/21797_front.jpg"),
        price="$35.00", company=company_1)
    session.add(sales_item_3)

    
    #SEGA
    company_2 = Company(
        name="SEGA", siteuri="http://www.sega.com/")
    session.add(company_2)

    sales_item_1 = SalesItem(
        name="Sonic 2",
        imageuri=("http://fc02.deviantart.net/fs71/f/2011/186/a/2/sonic_2_album_cover_by_death_cannon-d3l3248.jpg"),
        price="$45.00", company=company_2)
    session.add(sales_item_1)

    sales_item_2 = SalesItem(
        name="Earthworm Jim",
        imageuri=("http://img.gamefaqs.net/box/0/7/4/18074_front.jpg"),
        price="$40", company=company_2)
    session.add(sales_item_2)

    sales_item_3 = SalesItem(
        name="Alladin",
        imageuri=("http://gamesdbase.com/Media/SYSTEM/Sega_Nomad/Cart/big/Aladdin_-_1993_-_Sega.jpg"),
        price="$25", company=company_2)
    session.add(sales_item_3)


    #Activision
    company_3 = Company(
        name="Activision", siteuri="http://www.activision.com/")
    session.add(company_3)

    sales_item_1 = SalesItem(
        name="Spyro The Dragon",
        imageuri=("http://www.darkspyro.net/spyrothedragon/images/cover_jp_large.jpg"),
        price="$45.00", company=company_3)
    session.add(sales_item_1)

    sales_item_2 = SalesItem(
        name="Call Of Duty: Advanced Warfare",
        imageuri=("http://www.gamepur.com/files/imagepicker/6/thumbs/call-of-duty-advanced-warfare-cover-art.jpg"),
        price="$40", company=company_3)
    session.add(sales_item_2)

    sales_item_3 = SalesItem(
        name="Call Of Duty: Modern Warfare",
        imageuri=("http://www.game-ost.com/static/covers_soundtracks/2/3/23947_72392.jpg"),
        price="$60", company=company_3)
    session.add(sales_item_3)

    

    # commit all data at once
    session.commit()


if __name__ == '__main__':
    engine = create_engine('sqlite:///catalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    this_session = DBSession()
    load_default_data(this_session)
    print "added sales items!"
