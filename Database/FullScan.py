import scanVirtualMissions, scanTriviaWinners, scanParentsNightWinners, scanRCLAttendance, updateClassRF
import os

def main():
    while True:
        os.system('clear')
        scanRCLAttendance.main()
        scanVirtualMissions.main()
        scanTriviaWinners.main()
        scanParentsNightWinners.main()
        updateClassRF.main()

if __name__ == '__main__':
    main()
