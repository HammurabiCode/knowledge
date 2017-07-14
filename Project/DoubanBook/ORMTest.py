import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'mysql+pymysql://root:helloworld@127.0.0.1:3306/DB_TEST')

Base = declarative_base()


class Book(Base):

    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    sub_title = Column(String(128))
    pass


def init_db(): # create tables
    Base.metadata.create_all(engine)
    pass



def run():
    Session = sessionmaker(bind=engine)
    s = Session()
    s.add(Book(id =1, title='袁氏当国', sub_title=''))
    s.commit()
    s.close()
    pass

if __name__ == '__main__':
    # run()