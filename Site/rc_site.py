# pylint: disable=import-error
# pylint: disable=no-member
from flask import Flask, render_template, request
app = Flask(__name__)
import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import RCData as rcdata
import getTeamStats as getteamstats

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

@app.route('/team/<string:team_name>')
def show_team_stats(team_name):
    print('Loading information for team: '+team_name)
    team_data = getteamstats.get_team(team_name)
    member_names = getteamstats.get_members(team_name)
    weekly_nums = getteamstats.get_weekly_totals(team_name)
    weekly_missions = getteamstats.get_weekly_missions()
    print(weekly_nums)
    return render_template('team_stats.html',
            team_name=team_name,
            instructor_name=team_data[1],
            member_names=member_names,
            num_members=team_data[2],
            total_rf=team_data[3],
            
            num_robotics_overview=team_data[4],
            robotics_total = int(team_data[2]) * 30,
            robotics_percent = int(team_data[4])/(int(team_data[2])*30)*100,
            num_coding_overview=team_data[5],
            coding_overview_total = int(team_data[2]) * 30,
            coding_percent = int(team_data[5])/(int(team_data[2])*30)*100,
            num_python_1 = team_data[6],
            python_total = int(team_data[2]) * 50,
            python_percent = int(team_data[6])/(int(team_data[2])*30)*100,
            num_robotics_1 = team_data[7],
            robotics_1_total = int(team_data[2]) * 30,
            robotics_1_percent = int(team_data[7])/(int(team_data[2])*30)*100,
            num_entre_1 = team_data[8],
            entre_total = int(team_data[2]) * 15,
            entre_percent = int(team_data[8])/(int(team_data[2])*30)*100,
            total_vm_num = team_data[9],
            num_1 = weekly_nums[1],
            num_1_percent = int(weekly_nums[1])/int(team_data[2])*100,
            num_2 = weekly_nums[2],
            num_2_percent = int(weekly_nums[2])/int(team_data[2])*100,
            num_3 = weekly_nums[3],
            num_3_percent = int(weekly_nums[3])/int(team_data[2])*100,
            num_4 = weekly_nums[4],
            num_4_percent = int(weekly_nums[4])/int(team_data[2])*100,

            mission_1 = weekly_missions[0][0],
            mission_2 = weekly_missions[1][0],
            mission_3 = weekly_missions[2][0],
            mission_4 = weekly_missions[3][0]
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

            tvn1=lb_data[0][8],
            tvn2=lb_data[1][8],
            tvn3=lb_data[2][8],
            tvn4=lb_data[3][8],
            tvn5=lb_data[4][8],
            tvn6=lb_data[5][8],
            tvn7=lb_data[6][8],
            tvn8=lb_data[7][8],
            tvn9=lb_data[8][8],
            tvn10=lb_data[9][8],

            tvp1=lb_data[0][9],
            tvp2=lb_data[1][9],
            tvp3=lb_data[2][9],
            tvp4=lb_data[3][9],
            tvp5=lb_data[4][9],
            tvp6=lb_data[5][9],
            tvp7=lb_data[6][9],
            tvp8=lb_data[7][9],
            tvp9=lb_data[8][9],
            tvp10=lb_data[9][9],

            trn1=lb_data[0][10],
            trn2=lb_data[1][10],
            trn3=lb_data[2][10],
            trn4=lb_data[3][10],
            trn5=lb_data[4][10],
            trn6=lb_data[5][10],
            trn7=lb_data[6][10],
            trn8=lb_data[7][10],
            trn9=lb_data[8][10],
            trn10=lb_data[9][10],

            trp1=lb_data[0][11],
            trp2=lb_data[1][11],
            trp3=lb_data[2][11],
            trp4=lb_data[3][11],
            trp5=lb_data[4][11],
            trp6=lb_data[5][11],
            trp7=lb_data[6][11],
            trp8=lb_data[7][11],
            trp9=lb_data[8][11],
            trp10=lb_data[9][11],

            )



if __name__ == '__main__':
    app.run(host='0.0.0.0')
