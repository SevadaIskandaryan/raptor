import simple
from calibrator import Calibrator

def main():
    calibrator = Calibrator()
    calibrator.start_calibrator()

    simple.start("STATIC")


if __name__ == "__main__":
    main()