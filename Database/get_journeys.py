#########  Needed packages from GOOGLE  ############
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
####################################################
import pg8000, re, secret
import pgTool as pgtool
import RCData as rcdata
import random, string

sheet_id = '1VVK99xOwFIgHMqUlH-a1ZGrM1X2lIKlgMKc0cIi85Sw'

def connect():           
    db = pg8000.connect(secret.db['user'],
        password=secret.db['password'],       
        host=secret.db['host'],            
        port=secret.db['port'],            
        database=secret.db['database'])    
    db.run("SET TIMEZONE = 'EST'")
    return db

def twenty_four_certs(db,member_uuid):
    print('adding 24 cert')
    db.run(f"DELETE FROM journey_completions where member_uuid = '{member_uuid}'")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','blockchain')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','business_models')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','equity_debt')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','personal_corporate_taxes')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','branding_marketing')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','real_estate')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','trademarks_patents')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','global_economy')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','philanthropy')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','fintech')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','entertainment_gaming')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','global_food')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','artificial_intelligence')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','blockchain')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','the_universe')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','virtual_reality')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','future_of_internet')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','internet_of_things')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','deep_sea')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','3d_printing')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','renewable_energy')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','sustainability')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','robotics')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','future_of_coding')")

def twenty_certs(db,member_uuid):
    print('adding 20 cert')
    db.run(f"DELETE FROM journey_completions where member_uuid = '{member_uuid}'")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','blockchain')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','business_models')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','equity_debt')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','personal_corporate_taxes')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','branding_marketing')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','real_estate')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','trademarks_patents')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','global_economy')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','philanthropy')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','fintech')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','entertainment_gaming')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','global_food')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','artificial_intelligence')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','blockchain')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','virtual_reality')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','future_of_internet')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','3d_printing')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','renewable_energy')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','robotics')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','future_of_coding')")

def main():
    db = connect()
    data = rcdata.get_cells(sheet_id,'Q1:R27','certs')
    for line in data:
        num_certs = int(line[1])
        member_id = line[0]
        member_uuid = pgtool.get_member_uuid(member_id)
        print(member_id,member_uuid,num_certs)
        if member_uuid != -1:
            if num_certs == 20:
                twenty_certs(db,member_uuid)
            if num_certs == 24:
                twenty_four_certs(db,member_uuid)
    #db.commit()
    db.close()


if __name__ == '__main__':
    main()
