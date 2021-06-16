import scanVirtualMissions, scanTriviaWinners, scanParentsNightWinners, scanRCLAttendance, updateClassRF
import scanRCLOther, scanRFStore
import scanWheelWinners
import scanOldVirtualMissions
import getKahootScores

def main():
    while True:
        getKahootScores.main()
        scanRCLAttendance.main()
        scanVirtualMissions.main()
        scanRFStore.main()
        scanOldVirtualMissions.main()
        scanTriviaWinners.main()
        scanWheelWinners.main()
        scanParentsNightWinners.main()
        scanRCLOther.main()

if __name__ == '__main__':
    main()
