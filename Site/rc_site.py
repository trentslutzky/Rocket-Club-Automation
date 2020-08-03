# pylint: disable=import-error
# pylint: disable=no-member
from flask import Flask, render_template, request
app = Flask(__name__)
import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import RCData as rcdata

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
        print(member_id)
        # Get the data from the member stats sheet -->
        member_data = rcdata.site_get_cells(rcdata.member_stats_sheet_id, 'A2:1000')
        
        member_name = rcdata.get_member_info(member_data,member_id,'member_name')
        member_division = rcdata.get_member_info(member_data,member_id,'division')
        member_team = rcdata.get_member_info(member_data,member_id,'team')  
        #Get rocket fuel stuff
        #master_rf_sheet = rcdata.get_cells(rcdata.master_sheet_id, 'A2:1000')
        member_rf = rcdata.get_member_info(member_data,member_id,'total_rf') 
        trivia_rf = rcdata.get_member_info(member_data,member_id,'rc_live_trivia') 
        won_rf = rcdata.get_member_info(member_data,member_id,'wheel_of_names') 
        vm_rcl_attendance = rcdata.get_member_info(member_data,member_id,'rc_live_attendance') 
        boost_rf = rcdata.get_member_info(member_data,member_id,'boost') 
        rcgt_rf = rcdata.get_member_info(member_data,member_id,'rc_talent') 
        parents_rf = rcdata.get_member_info(member_data,member_id,'rc_live_pn')
        class_rf = rcdata.get_member_info(member_data,member_id,'class') 
        #Get totals for virtual mission categories
        vm_total = rcdata.get_member_info(member_data,member_id,'virtual_missions') 

        num_robotics_overview = rcdata.get_member_info(member_data,member_id,'num_robotics_overview')
        num_coding = rcdata.get_member_info(member_data,member_id,'num_coding_overview')
        num_python = rcdata.get_member_info(member_data,member_id,'num_python_1')
        num_robotics_1 = rcdata.get_member_info(member_data,member_id,'num_robotics_1')
        num_entre = rcdata.get_member_info(member_data,member_id,'num_entre_1')


        if(member_name != 'null'):
            member_rf =str(format(int(member_rf),','))
            return render_template('stats.html', 
            name = member_name, 
            division = member_division, 
            team = member_team, 
            rf_total = member_rf,
            rf_vm = vm_total,
            n_robotics = num_robotics_overview,
            n_coding = num_coding,
            n_python = num_python,
            n_robotics_1 = num_robotics_1,
            n_entre = num_entre,
            rf_rcl_attendance = vm_rcl_attendance,
            rf_trivia = trivia_rf,
            rf_won = won_rf,
            rf_rcl_total = str(int(vm_rcl_attendance) + int(trivia_rf) + int(won_rf)),
#            rf_rcl_total = 0,
            rf_boost = boost_rf,
            rf_rcgt = rcgt_rf,
            rf_parents = parents_rf,
            rf_class = class_rf
            )
        else:
            return render_template('oops.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0')
