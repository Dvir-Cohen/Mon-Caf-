
import sys
import os
if os.path.isfile('moncafe.db'):
        os.remove('moncafe.db')
from repository import repo


def main(argv):

    repo.create_tables(argv)



if __name__ == "__main__":
    main(sys.argv[1])