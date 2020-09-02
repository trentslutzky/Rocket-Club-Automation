import scanVirtualMissions, scanTriviaWinners, scanParentsNightWinners, scanRCLAttendance, updateClassRF

def main():
    scanRCLAttendance.main()
    scanVirtualMissions.main()
    scanTriviaWinners.main()
    scanParentsNightWinners.main()
    updateClassRF.main()

if __name__ == '__main__':
    main()
