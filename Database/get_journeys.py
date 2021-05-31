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

sheet_id = '1HeY8PtFUhA1CRHqovigV3Ds_sDpdruL5ZlZxC5IIAvE'

def connect():           
    db = pg8000.connect(secret.db['user'],
        password=secret.db['password'],       
        host=secret.db['host'],            
        port=secret.db['port'],            
        database=secret.db['database'])    
    db.run("SET TIMEZONE = 'EST'")
    return db

def one_cert(db,member_uuid):
    print('adding one cert')
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','artificial_intelligence')")

def three_certs(db,member_uuid):
    print('adding 3 cert')
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','artificial_intelligence')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','the_stock_market')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','blockchain')")

def nine_certs(db,member_uuid):
    print('adding 9 cert')
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','artificial_intelligence')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','the_stock_market')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','blockchain')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','business_models')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','equity_debt')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','personal_corporate_taxes')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','branding_marketing')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','real_estate')")
    db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','trademarks_patents')")

def main():
    db = connect()
    data = rcdata.get_cells(sheet_id,'Q1:R','certs')
    for line in data:
        num_certs = int(line[1])
        member_id = line[0]
        member_uuid = pgtool.get_member_uuid(member_id)
        print(member_id,member_uuid,num_certs)
        if member_uuid != -1:
            if num_certs == 1:
                one_cert(db,member_uuid)
            if num_certs == 3:
                three_certs(db,member_uuid)
            if num_certs == 9:
                nine_certs(db,member_uuid)
    db.commit()
    db.close()


if __name__ == '__main__':
    main()
