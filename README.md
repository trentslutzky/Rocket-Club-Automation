 # A potential way to automate the Rocket Fuel process using Google drive APIs and Python

This script scans the folder of Virtual Missions Google Forms responses 
and automatically adds rocket fuel to the master sheet.

the script could be on a cron job, and automatically run once a day at night when the kids are asleep.

__This should make the Google Shees much faster, as there aren't tons of formulas within each cell.__

## Requirements
   
   Forms/Responses folder organized like the example.
   
   Master Sheet organized in a specific (simple) way.

## TO DO:

    [x] Automate adding Virtual Missions rocket fuel to master sheet
        [ ] Implement weekly totals for use in leaderboards
    [ ] Instead of hard-coding ranges, use table titles to figure out where data is...
    [x] Implement RC Live Winners
        [ ] Optimize the way the spreadsheet is dealth with 
    [ ] Print to the console the Rocket Fuel leader afeter refreshing

screenshot of the process running:

<img src="https://github.com/trentslutzky/Rocket-Club-Automation/blob/master/images/sc1.png" width=620>
