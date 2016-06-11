#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

eng = create_engine('sqlite:///healthscores_db.db')
Base = declarative_base()

class healthdata(Base):
    __tablename__ = "Scores"
    Nonsmoking = Column(String)
    Name = Column(String, primary_key=True) 
    Type = Column(String)  
    Address = Column(String)
    Score = Column(Integer)
    Latest_Inspec_Date = Column(String)
    Past_Scores_Link = Column(String)
    Latest_Inspec_Link = Column(String)
        
Base.metadata.bind = eng        
Base.metadata.create_all()        
        
Session = sessionmaker(bind=eng)
ses = Session()

def add_row(row_data):
    sess = Session() 

    for entries in row_data:
        restaurants = healthdata(Nonsmoking=entries[0], Name=entries[1], Type=entries[2], Address=entries[3], Score=entries[4],Latest_Inspec_Date=entries[5],Past_Scores_Link=entries[6],Latest_Inspec_Link=entries[7])
        lookup_name = ses.query(healthdata).filter(healthdata.Name==entries[1]).all()
        #Check to see is entry exists, if not, add.
        if not lookup_name:
            sess.add(restaurants)
            sess.commit()
        #Entry already exists, check to see if date is different
        else:
            #retrieve date of latest inspection
            for instance in sess.query(healthdata).filter(healthdata.Name==entries[1]):
                score_date = instance.Latest_Inspec_Date
            #compare latest inspec date in db to scraped date and update if !=
            if score_date != entries[5]:
                sess.query(healthdata).\
                    filter(healthdata.Name==entries[1]).\
                    update({"Score":entries[4],"Latest_Inspec_Date":entries[5],"Past_Scores_Link":entries[6],"Latest_Inspec_Link":entries[7]})
                sess.commit()    
    sess.close()

def json_formatter():
    data_set = ses.query(healthdata).all()
    listofrows = []
    for data in data_set:
        datarow = {
            'name': data.Name,
            'type': data.Type,
            'address': data.Address,
            'smokeYN': data.Nonsmoking,
            'score': data.Score,
            'scoreDate': data.Latest_Inspec_Date,
            'currScoreLink': data.Latest_Inspec_Link,
            'pastScoreLink': data.Past_Scores_Link,
        }
        listofrows.append(datarow)
    return json.dumps(listofrows)

