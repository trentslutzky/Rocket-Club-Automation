import sys

sys.path.append("..")

import pgTool as pgtool
import pg8000
import rcCerts as rccerts

certs = ['financial_projections',
         'business_models',
         'branding',
         'market_positioning_map',
         'marketing_mix',
         'personal_relations',
         'business_valuation_stock',
         'equity_debt_financing_fund_raising_rounds',
         'angel_venture_capitalists',
         'mergers_aquisitions',
         'personal_selling']

def connect():
    db = pg8000.connect("postgres", 
        password="Falcon2019", 
        host='35.199.36.16', 
        port=5432, 
        database='rocket_club')
    return db

def qprep(db, string):
    db.run("DEALLOCATE ALL")
    result = db.prepare(string)
    return result

def get_member_ids():
    db = connect()
    try:
        ps = qprep(db,'SELECT member_id FROM members')
        result = ps.run()
        return result
    except:
        return -1
    db.close()

def mass_update():
    print(certs)
    member_ids = get_member_ids()
    for m_id in member_ids:
        member_id = m_id[0]
        rccerts.update_certs(member_id,certs)


def main():
    print('This changes certifications for EVERY rocket club member. Are you sure?')
    print('(type "yes" to run)',end=' ')
    query = input()
    if(query == 'yes'):
        print('Mass updating. This could take a while...')
        mass_update()
    else:
        print('exiting.')



if __name__ == '__main__':
    main()
