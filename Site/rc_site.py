# pylint: disable=import-error
# pylint: disable=no-member
from flask import Flask, render_template, request
app = Flask(__name__)
import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import RCData as rcdata
import getTeamStats as getteamstats

import pgTool as pgtool
import time

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        member_id = request.form['member-id']
        print(member_id)

    return render_template('gate.html')

@app.route('/stats', methods=['GET', 'POST'])
def show_stats():
    if request.method == 'POST':
        
        #Get member name, team, division
        member_id = request.form['member-id']
        print('Loading stats page for ' + member_id)
        # Get the data from the member stats sheet -->
        #member_data = rcdata.site_get_cells(rcdata.member_stats_sheet_id, 'A2:1000')
        
        #member_name = rcdata.get_member_info(member_data,member_id,'member_name')
        #member_division = rcdata.get_member_info(member_data,member_id,'division')
        #member_team = rcdata.get_member_info(member_data,member_id,'team')  
        #Get rocket fuel stuff
        #master_rf_sheet = rcdata.get_cells(rcdata.master_sheet_id, 'A2:1000')
        #member_rf = rcdata.get_member_info(member_data,member_id,'total_rf') 
        #trivia_rf = rcdata.get_member_info(member_data,member_id,'rc_live_trivia') 
        #won_rf = rcdata.get_member_info(member_data,member_id,'wheel_of_names') 
        #vm_rcl_attendance = rcdata.get_member_info(member_data,member_id,'rc_live_attendance') 
        #boost_rf = rcdata.get_member_info(member_data,member_id,'boost') 
        #rcgt_rf = rcdata.get_member_info(member_data,member_id,'rc_talent') 
        #parents_rf = rcdata.get_member_info(member_data,member_id,'rc_live_pn')
        #class_rf = rcdata.get_member_info(member_data,member_id,'class') 
        #Get totals for virtual mission categories
        #vm_total = rcdata.get_member_info(member_data,member_id,'virtual_missions') 

        #num_robotics_overview = rcdata.get_member_info(member_data,member_id,'num_robotics_overview')
        #num_coding = rcdata.get_member_info(member_data,member_id,'num_coding_overview')
        #num_python = rcdata.get_member_info(member_data,member_id,'num_python_1')
        #num_robotics_1 = rcdata.get_member_info(member_data,member_id,'num_robotics_1')
        #num_entre = rcdata.get_member_info(member_data,member_id,'num_entre_1')
            
        # Member info from pgtool
        member_info = pgtool.get_member_info(member_id)
        # Member total RF
        member_rf = pgtool.get_member_total(member_id)
        # Member Virtual Mission RF
        vm_total = pgtool.get_vm_total_rf(member_id)
        # VMs completed
        vm_completions = pgtool.get_member_vms_completed(member_id)
        # RCL RF
        rcl_rf = pgtool.get_member_rcl_rf(member_id)
        # MISC RF
        misc_rf = pgtool.get_member_misc_rf(member_id)
        
        try:
            member_rf =str(format(int(member_rf),','))
            return render_template('stats.html', 
            name = member_info[0], 
            division = member_info[1], 
            team = member_info[2], 
            rf_total = member_rf,
            rf_vm = vm_total,
            n_robotics = vm_completions[0],
            n_coding = vm_completions[1],
            n_python = vm_completions[2],
            n_robotics_1 = vm_completions[3],
            n_entre = vm_completions[4],
            rf_rcl_attendance = rcl_rf[1],
            rf_trivia = rcl_rf[2],
            rf_won = misc_rf[2],
            rf_rcl_total = rcl_rf[0],
#            rf_rcl_total = 0,
            rf_boost = misc_rf[0],
            rf_rcgt = misc_rf[1],
            rf_parents = rcl_rf[3],
            rf_class = misc_rf[3]
            )
        except:
            return render_template('oops.html')

@app.route('/team/<string:team_name>')
def show_team_stats(team_name):
    print('Loading information for team: '+team_name)
    
    member_names = pgtool.get_team_members(team_name)
    num_members = len(member_names)
    instructor = pgtool.get_instructor(team_name)
    
    weekly_missions = pgtool.get_weekly_missions()
    weekly_completions = pgtool.get_current_weekly_missions_completed(team_name)
    vms_completed = pgtool.get_team_vms_completed(team_name)

    return render_template('team_stats.html',
            team_name=team_name,
            instructor_name=instructor,
            member_names=member_names,
            num_members=num_members,
            
            num_robotics_overview=vms_completed[0],
            robotics_total = int(num_members) * 30,
            robotics_percent = int(vms_completed[0])/(int(num_members)*30)*100,

            num_coding_overview=vms_completed[1],
            coding_overview_total = int(num_members) * 30,
            coding_percent = int(vms_completed[1])/(int(num_members)*30)*100,
            
            num_python_1 = vms_completed[2],
            python_total = int(num_members) * 50,
            python_percent = int(vms_completed[2])/(int(num_members)*30)*100,
            
            num_robotics_1 = vms_completed[3],
            robotics_1_total = int(num_members) * 30,
            robotics_1_percent = int(vms_completed[3])/(int(num_members)*30)*100,
            
            num_entre_1 = vms_completed[4],
            entre_total = int(num_members) * 15,
            entre_percent = int(vms_completed[4])/(int(num_members)*30)*100,
            
            num_1 = weekly_completions[0],
            num_1_percent = int(weekly_completions[0])/int(num_members)*100,
            num_2 = weekly_completions[1],
            num_2_percent = int(weekly_completions[1])/int(num_members)*100,

            mission_1 = weekly_missions[0],
            mission_2 = weekly_missions[1]
            )

@app.route('/leaderboard')
def show_leaderboard():
    lb_data = rcdata.get_cells('1t8hVPvUQ_Wca1nIiVMovsZFb20I2kcYjJGfp8E7ctS0','full_leaderboard')
    #get top ten table

    return render_template('leaderboard.html',
            ttn1=lb_data[0][0],
            ttn2=lb_data[1][0],
            ttn3=lb_data[2][0],
            ttn4=lb_data[3][0],
            ttn5=lb_data[4][0],
            ttn6=lb_data[5][0],
            ttn7=lb_data[6][0],
            ttn8=lb_data[7][0],
            ttn9=lb_data[8][0],
            ttn10=lb_data[9][0],
            ttrf1=lb_data[0][1],
            ttrf2=lb_data[1][1],
            ttrf3=lb_data[2][1],
            ttrf4=lb_data[3][1],
            ttrf5=lb_data[4][1],
            ttrf6=lb_data[5][1],
            ttrf7=lb_data[6][1],
            ttrf8=lb_data[7][1],
            ttrf9=lb_data[8][1],
            ttrf10=lb_data[9][1],

            d1n1=lb_data[0][2],
            d1n2=lb_data[1][2],
            d1n3=lb_data[2][2],
            d1rf1=lb_data[0][3],
            d1rf2=lb_data[1][3],
            d1rf3=lb_data[2][3],

            d2n1=lb_data[0][4],
            d2n2=lb_data[1][4],
            d2n3=lb_data[2][4],
            d2rf1=lb_data[0][5],
            d2rf2=lb_data[1][5],
            d2rf3=lb_data[2][5],

            d3n1=lb_data[0][6],
            d3n2=lb_data[1][6],
            d3n3=lb_data[2][6],
            d3rf1=lb_data[0][7],
            d3rf2=lb_data[1][7],
            d3rf3=lb_data[2][7],

            t1vn1=lb_data[0][8],
            t1vn2=lb_data[1][8],
            t1vn3=lb_data[2][8],
            t1vn4=lb_data[3][8],
            t1vn5=lb_data[4][8],
            t1vn6=lb_data[5][8],

            t1vp1=lb_data[0][9],
            t1vp2=lb_data[1][9],
            t1vp3=lb_data[2][9],
            t1vp4=lb_data[3][9],
            t1vp5=lb_data[4][9],
            t1vp6=lb_data[5][9],
            
            t2vn1=lb_data[0][10],
            t2vn2=lb_data[1][10],
            t2vn3=lb_data[2][10],
            t2vn4=lb_data[3][10],
            t2vn5=lb_data[4][10],
            t2vn6=lb_data[5][10],

            t2vp1=lb_data[0][11],
            t2vp2=lb_data[1][11],
            t2vp3=lb_data[2][11],
            t2vp4=lb_data[3][11],
            t2vp5=lb_data[4][11],
            t2vp6=lb_data[5][11],

            t3vn1=lb_data[0][12],
            t3vn2=lb_data[1][12],
            t3vn3=lb_data[2][12],
            t3vn4=lb_data[3][12],
            t3vn5=lb_data[4][12],
            t3vn6=lb_data[5][12],

            t3vp1=lb_data[0][13],
            t3vp2=lb_data[1][13],
            t3vp3=lb_data[2][13],
            t3vp4=lb_data[3][13],
            t3vp5=lb_data[4][13],
            t3vp6=lb_data[5][13],

            trivian1=lb_data[0][14],
            trivian2=lb_data[1][14],
            trivian3=lb_data[2][14],
            trivian4=lb_data[3][14],
            trivian5=lb_data[4][14],
            triviarf1=lb_data[0][15],
            triviarf2=lb_data[1][15],
            triviarf3=lb_data[2][15],
            triviarf4=lb_data[3][15],
            triviarf5=lb_data[4][15],

            parentsn1=lb_data[0][16],
            parentsn2=lb_data[1][16],
            parentsn3=lb_data[2][16],
            parentsn4=lb_data[3][16],
            parentsn5=lb_data[4][16],
            parentsrf1=lb_data[0][17],
            parentsrf2=lb_data[1][17],
            parentsrf3=lb_data[2][17],
            parentsrf4=lb_data[3][17],
            parentsrf5=lb_data[4][17]
            )



if __name__ == '__main__':
    app.run(host='0.0.0.0')
