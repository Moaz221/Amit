"""Simple data preprocessing functions for beginner-level assignments."""

import pandas as pd


def Read_data_file(file_path):
    """Read a CSV file and return a pandas DataFrame.

    Args:
        file_path: The path to the CSV file to read.

    Returns:
        A pandas DataFrame containing the file data, or None if the file could not be read.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except OSError:
        print(f"Error: Invalid file path or file cannot be opened: {file_path}")
    except ValueError:
        print(f"Error: Invalid file path or CSV content: {file_path}")
    except pd.errors.EmptyDataError:
        print(f"Error: The file is empty or has no data: {file_path}")

    return None


def Drop_unnecessary_features(df, cols_to_drop):
    """Remove the requested columns from a DataFrame.

    Args:
        df: The pandas DataFrame to modify.
        cols_to_drop: A list of column names to remove.

    Returns:
        The DataFrame after removing valid columns. Missing columns are skipped with a warning.
    """
    if df is None:
        return None

    if not cols_to_drop:
        return df

    for column in cols_to_drop:
        if column in df.columns:
            df = df.drop(columns=[column])
        else:
            print(f"Warning: Column '{column}' was not found and was skipped.")

    return df


def Check_data_type(df):
    """Create a simple data-quality report for all columns.

    Args:
        df: The pandas DataFrame to inspect.

    Returns:
        A transposed DataFrame showing each column's data type and number of unique values.
    """
    if df is None:
        return None

    report = pd.DataFrame({
        "data_type": df.dtypes.astype(str),
        "unique_values": df.nunique()
    })

    return report.T
