from colorama import init
init()
from colorama import Fore, Back, Style

import RCData as rcdata

##### Formulas for the different columns in master sheet ########
total_rf_formula = '=SUM(F#:P#)-E#'
status_formula = '=VLOOKUP(A#,\'Base RF\'!A1:100#,4,False)'
virtual_missions_formula = '=IMPORTRANGE(\"1rVblBZu9FXzM9guC9R5CxQEtYlTN_NGfFiv2X4ivh70\",\"C#\")'
class_formula = '=VLOOKUP(A#,\'Base RF\'!A1:100#,8,False)'
wheel_of_names_formula = '=VLOOKUP(A#,\'Base RF\'!A1:100#,7,False)'
rc_talent_formula = '=VLOOKUP(A#,\'Base RF\'!A1:100#,13,False)'
boost_formula = '=VLOOKUP(A#,\'Base RF\'!A1:100#,14,False)' 
#################################################################

def addNumber(formula, number):
    new_formula = formula.replace('#',str(number))
    return new_formula 

def main():
    master_sheet = rcdata.get_cells(rcdata.master_sheet_id, 'A2:1000')
    total_col = master_sheet[0].index('total_rf')
    status_col = master_sheet[0].index('status')
    vm_col = master_sheet[0].index('virtual_missions')
    class_col = master_sheet[0].index('class')
    wheel_col = master_sheet[0].index('wheel_of_names')
    talent_col = master_sheet[0].index('rc_talent')
    boost_col = master_sheet[0].index('boost')
    for row in master_sheet:
        r = str(master_sheet.index(row)+2)
        if(int(r) > 2):
            row[total_col] = addNumber(total_rf_formula,r)
            row[status_col] = addNumber(status_formula,r)
            row[vm_col] = addNumber(virtual_missions_formula,r)
            row[class_col] = addNumber(class_formula,r)
            row[wheel_col] = addNumber(wheel_of_names_formula,r)
            row[talent_col] = addNumber(rc_talent_formula,r)
            row[boost_col] = addNumber(boost_formula,r)
    
    rcdata.set_cells(rcdata.master_sheet_id, 'A2:1000',master_sheet)

if __name__ == '__main__':
    main()
