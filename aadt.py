import argparse
from src.algorithm import AADT
from src.parse import parse_dances, parse_preferences


def main():
    parser = argparse.ArgumentParser(description="Process preferences and dances files.")
    parser.add_argument("preferences_file", type=str, help="Preferences file (csv format)")
    parser.add_argument("dances_file", type=str, help="Dances file (csv format)")
    args = parser.parse_args()

    dancers = parse_preferences(args.preferences_file)
    dances = parse_dances(args.dances_file)

    algorithm = AADT(dancers, dances)
    algorithm.phase_1()
    algorithm.export_assignments("phase1.xlsx")
    algorithm.phase_2()
    algorithm.export_assignments("phase2.xlsx")

if __name__ == "__main__":
    main()