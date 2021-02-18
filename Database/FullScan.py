import scanVirtualMissions, scanTriviaWinners, scanParentsNightWinners, scanRCLAttendance, updateClassRF
import scanRCLOther, scanRFStore
import scanWheelWinners
import scanOldVirtualMissions
import random
import rich
from rich.console import Console

console = Console()

spinner = 'earth'

def randomSpinner():
    spinners = [
            'aesthetic',
            'arc',
            'arrow',
            'arrow2',
            'arrow3',
            'balloon',
            'balloon2',
            'betaWave',
            'bounce',
            'bouncingBall',
            'bouncingBar',
            'boxBounce',
            'boxBounce2',
            'christmas',
            'clock',
            'dots',
            'dots12',
            'earth',
            'line',
            'material',
            'point',
            'pong',
            'runner',
            'shark',
            'moon'
            ]
    return str(random.choice(spinners))

def main():
    while True:
        scanRCLAttendance.main()
        scanVirtualMissions.main()
        scanRFStore.main()
        scanOldVirtualMissions.main()
        scanTriviaWinners.main()
        scanWheelWinners.main()
        scanParentsNightWinners.main()
        updateClassRF.main()
        scanRCLOther.main()

if __name__ == '__main__':
    main()
