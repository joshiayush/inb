from console.print import printRed
from console.print import printBlue
from console.print import printGreen

from tests.linkedintest import test_linkedin
from tests.linkedinconnectionsautotest import test_linkedin_connections_auto


def start_testing() -> None:
    total = 0
    success = 0
    failed = 0

    print()

    printGreen("> testing linkedin-bot@1.31.15 ...", style='b')

    print()
    _total, _success, _failed = test_linkedin()
    print()

    total += _total
    success += _success
    failed += _failed

    print()
    _total, _success, _failed = test_linkedin_connections_auto()
    print()

    total += _total
    success += _success
    failed += _failed

    printBlue("Total tests: " + str(total), style='b')
    printGreen("Success: " + str(success), style='b')
    printRed("Failed: " + str(failed), style='b')


if __name__ == "__main__":
    start_testing()
