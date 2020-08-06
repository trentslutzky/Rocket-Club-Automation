import RCData as rcdata

team_stats_sheet_id = '1psE8lGsQl_qihUg7EYLDaD_DyfSajfWSlsVtfUvVqAA'
member_stats_sheet_id = '1UkJKMY735oTSohu8X5eM_rvFp267KBbaEiVg4SXaki8'

def get_team(team_name):
    team_info = rcdata.site_get_cells(team_stats_sheet_id,'team_stats')
    num_col = team_info[0].index('num')
    inst_col = team_info[0].index('instructor')
    n1_col = team_info[0].index('num_robotics_overview')
    n1_col = team_info[0].index('num_coding_overview')
    n1_col = team_info[0].index('num_python_1')
    n1_col = team_info[0].index('num_robotics_1')
    n1_col = team_info[0].index('num_entre_1')

    for row in team_info:
        if row[0] == team_name:
            return row

def get_members(team_name):
    team_members = []
    member_stats_data = rcdata.get_cells(member_stats_sheet_id,'A2:1000')
    name_col = member_stats_data[0].index('member_name')
    team_col = member_stats_data[0].index('team')
    for row in member_stats_data:
        if row[team_col] == team_name:
            team_members.append(row[name_col])
    return team_members

def main():
    print(get_members('Supernovas'))

if __name__ == '__main__':
    main()
