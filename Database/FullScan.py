import scanVirtualMissions, scanTriviaWinners, scanParentsNightWinners, scanRCLAttendance, updateClassRF
import scanRCLOther
import scanWheelWinners
import scanOldVirtualMissions
import random
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
            'dots1',
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
    stat = ''
    while True:
        stat = 'RCL Attendance'
        with console.status("Updating [bold green]"+stat,randomSpinner()) as status:
            scanRCLAttendance.main()
        stat = 'Virtual Missions'
        with console.status("Updating [bold green]"+stat,randomSpinner()) as status:
            scanVirtualMissions.main()
            scanOldVirtualMissions.main()
        stat = 'Trivia Winners'
        with console.status("Updating [bold green]"+stat,randomSpinner()) as status:
            scanTriviaWinners.main()
        stat = 'Wheel Winners'
        with console.status("Updating [bold green]"+stat,randomSpinner()) as status:
            scanWheelWinners.main()
        stat = 'Parents Night'
        with console.status("Updating [bold green]"+stat,randomSpinner()) as status:
            scanParentsNightWinners.main()
        stat = 'Class RF'
        with console.status("Updating [bold green]"+stat,randomSpinner()) as status:
            updateClassRF.main()
        stat = 'Other stuff'
        with console.status("Updating [bold green]"+stat,randomSpinner()) as status:
            scanRCLOther.main()

if __name__ == '__main__':
    main()
