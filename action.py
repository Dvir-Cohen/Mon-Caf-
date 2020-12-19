
import sys

from printdb import printdb
from repository import repo


def main(argv):

    repo.insertActivities(argv)
    repo._conn.commit()
    printdb()

if __name__ == "__main__":
    main(sys.argv[1])