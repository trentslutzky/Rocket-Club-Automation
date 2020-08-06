import RCData as rcdata

team_stats_sheet_id = '1psE8lGsQl_qihUg7EYLDaD_DyfSajfWSlsVtfUvVqAA'
member_stats_sheet_id = '1UkJKMY735oTSohu8X5eM_rvFp267KBbaEiVg4SXaki8'

def get_team(team_name):
    team_info = rcdata.site_get_cells(team_stats_sheet_id,'team_stats')
    
    for row in team_info:
        if row[0] == team_name:
            return row

def get_weekly_totals(team_name):
    team_weekly_nums = rcdata.site_get_cells(team_stats_sheet_id,'weekly_totals')
    for row in team_weekly_nums:
        if row[0] == team_name:
            return row

def get_weekly_missions():
    weekly_missions = rcdata.get_cells(team_stats_sheet_id,'weekly_missions')
    return weekly_missions

def get_members(team_name):
    team_members = []
    member_stats_data = rcdata.get_cells(member_stats_sheet_id,'A2:1000')
    name_col = member_stats_data[0].index('member_name')
    team_col = member_stats_data[0].index('team')
    for row in member_stats_data:
        if row[team_col] == team_name:
            team_members.append(row[name_col])
    return team_members

        
if __name__ == '__main__':
    main()
