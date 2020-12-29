# pylint: disable=no-member
# pylint: disable=unused-variable
import RCData as rcdata
import pgTool as pgtool
import pg8000
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style

#####################################################################
## connecting to the database as the root user 'postgres'
db = pg8000.connect("postgres", 
        password="Falcon2019", 
        host='35.199.36.16', 
        port=5432, 
        database='rocket_club')

########### Virtual Missions Folder IDs ############
coding_vm_folder_id = "'1SG63RmmC42yQ_eR_-dq9IPfWC83DsRbg'"
vm_robotics_overview_folder_id = "'1PLs-Uu77I2TTZifpH7MmNwEg2u4YUzsl'"
python_1_folder_id = "'18f6ymu1kSSkQ4Pjh5HcEgsTGTxINYlUn'"
robotics_1_folder_id = "'1JGJGuxyur9Jyl_GZjMa6qjNQBU4tOjcp'"
ent_1_folder_id = "'1ETN-kZrBEygQfHkcP70uIH9sHMW5Iw93'"
extra_folder_id = "'1fdjZTAqrUnNWm_dQb38zE6VrXk7MJNPF'"

def scan_folder(category,folder_id):
    completions = []
    new_q = folder_id + " in parents"
    results = rcdata.drive_service.files().list(q = new_q, 
                                    fields='nextPageToken, files(id, name)',
                                    pageToken=None).execute()
    sort_folder(results)

def sort_folder(folder):
    vms = []
    for sheet in folder.get('files', []):
        sheet_id = sheet['id']
        
        sheet_name = sheet['name']
        sheet_name = sheet_name.replace('  (Responses)','')
        sheet_name = sheet_name.replace(' (Responses)','')
        sheet_name = sheet_name[:41]
        sheet_name = sheet_name[22:]
        sheet_name = sheet_name.replace(' | Mission','')

        vm_num = sheet_name[7:]
        vm_tag = 'python_1_' + vm_num

        if(sheet_name != 'Unused'):
            vm = [0,'','','']
            vm[0] = int(vm_num)
            vm[1] = sheet_id
            vm[2] = sheet_name
            vm[3] = vm_tag
            vms.append(vm)

            updateVirtualMission(vm_tag,sheet_name,sheet_id)

    vms.sort(key=getName)
    for vm in vms:
        print(vm)

def getName(e):
    return e[0]

def updateVirtualMission(vm_tag,name,sheet_id):
    command = ("UPDATE virtual_missions SET description='%s', sheet_id='%s' WHERE vm_tag='%s'"
    % (name,sheet_id,vm_tag))
    print(command)
    db.run(command)
    db.commit()

def main():
    print('|                 SHEET ID                  |   NAME  |   vm_tag    |')
    scan_folder('python_1',python_1_folder_id)
    updateVirtualMission('python_1_50','Python 50','TEST TEST')


if __name__ == '__main__':
    main()
