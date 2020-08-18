# pylint: disable=import-error
# pylint: disable=no-member
from flask import Flask, render_template, request
app = Flask(__name__)
import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

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
        
        if member_rf == None:
            member_id = 0
        else:
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
    #get top ten table
    team_standings = pgtool.get_team_standings()
    division_standings = pgtool.get_division_standings()
    legacy_leaders = pgtool.get_legacy_leaders()
    trivia_leaders = pgtool.get_trivia_leaders()
    parents_night_leaders = pgtool.get_parents_night_leaders()

    return render_template('test_leaderboard.html',
                team_standings=team_standings,
                division_standings=division_standings,
                legacy_leaders=legacy_leaders,
                trivia_leaders=trivia_leaders,
                parents_night_leaders=parents_night_leaders
            )



if __name__ == '__main__':
    app.run(host='0.0.0.0')
