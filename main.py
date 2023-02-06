# import sqlalchemy
# from sqlalchemy.orm import sessionmaker
# from models import create_tables, Publisher, Book, Shop, Stock, Sale
# import json
#
# DSN = "postgresql://postgres:admin@localhost:5432/ormdb"
# engine = sqlalchemy.create_engine(DSN)
# create_tables(engine)
#
# # сессия
# Session = sessionmaker(bind=engine)
# session = Session()
#
# with open('tests_data.json', 'r') as td:
#     data = json.load(td)
#
# for item in data:
#     tables={
#         'publisher': Publisher,
#         'book': Book,
#         'shop': Shop,
#         'stock': Stock,
#         'sale': Sale}[item.get('tables')]
#     session.add(tables(id=item.get('pk'), **item.get('fields')))
#
# session.commit()
#
# publisher_input = input('Введите имя или идентификатор издателя: ')
#
# for book, shop, price, date in session.query(
#     Book.title,
#     Shop.name,
#     Sale.price,
#     Sale.date_sale).join(
#         Publisher, Book.id_publisher == Publisher.id).join(
#             Stock, Book.id == Stock.id_book).join(
#                 Shop, Shop.id == Stock.id_book).join(
#                     Sale, Stock.id == Sale.id_stock).filter(
#                         Publisher.name == publisher_input):
#     print(f'{book} | {shop} | {price} | {date}')
#
# session.close()


import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:admin@localhost:5432/ormdb'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session  = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()

publisher_input = input('Введите имя или идентификатор издателя: ')

for book, shop, price, date in session.query(
    Book.title,
    Shop.name,
    Sale.price,
    Sale.date_sale).join(
        Publisher, Book.id_publisher == Publisher.id).join(
            Stock, Book.id == Stock.id_book).join(
                Shop, Shop.id == Stock.id_book).join(
                    Sale, Stock.id == Sale.id_stock).filter(
                        Publisher.name == publisher_input):
    print(f'{book} | {shop} | {price} | {date}')

session.close()