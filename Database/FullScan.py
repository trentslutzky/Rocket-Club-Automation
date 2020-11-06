import scanVirtualMissions, scanTriviaWinners, scanParentsNightWinners, scanRCLAttendance, updateClassRF
import scanRCLOther
import os

def main():
    while True:
        os.system('clear')
        scanRCLAttendance.main()
        scanVirtualMissions.main()
        scanTriviaWinners.main()
        scanParentsNightWinners.main()
        updateClassRF.main()
        scanRCLOther.main()

if __name__ == '__main__':
    main()
