import sys
import os

main_dir = os.path.dirname(__file__)
sys.path.append(main_dir)


if __name__ == '__main__':
    for pth in sys.path:
        print(pth)
