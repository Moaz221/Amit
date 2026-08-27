"""Simple Titanic preprocessing menu for students."""

from pathlib import Path

from config.config import COLS_TO_DROP
from preprocessing import Check_data_type, Drop_unnecessary_features, Read_data_file


def main():
    """Run the main menu for the Titanic dataset preprocessing workflow."""
    dataset_path = Path(__file__).resolve().parent / "data" / "raw" / "titanic.csv"
    df = None

    while True:
        print("\n===== Titanic Data Preprocessing =====")
        print("1. Read Dataset")
        print("2. Remove Unnecessary Features")
        print("3. Check Data Types")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            df = Read_data_file(dataset_path)
            if df is not None:
                print("Dataset loaded successfully.")
                print(df.head())

        elif choice == "2":
            if df is None:
                print("Please read the dataset first.")
                continue

            answer = input("Do you want to remove the configured columns? (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                df = Drop_unnecessary_features(df, COLS_TO_DROP)
                print("Unnecessary features removed.")
                print(df.head())
            else:
                print("No columns were removed.")

        elif choice == "3":
            if df is None:
                print("Please read the dataset first.")
                continue

            data_quality_report = Check_data_type(df)
            print("\nData Quality Report:")
            print(data_quality_report)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()
