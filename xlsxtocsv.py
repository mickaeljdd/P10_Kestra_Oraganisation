import pandas as pd


def convert_excel_to_csv(excel_file, csv_file):
    dataframe = pd.read_excel(excel_file)
    dataframe.to_csv(csv_file, index=False, header=True)
    return dataframe


if __name__ == "__main__":
    add_rep = "./input/"
    list_of_excel_files = ["Fichier_erp.xlsx", "fichier_liaison.xlsx", "Fichier_web.xlsx"]
    list_of_csv_files = ["Fichier_erp.csv", "fichier_liaison.csv", "Fichier_web.csv"]
    for excel_file, csv_file in zip(list_of_excel_files, list_of_csv_files):
        print(add_rep + excel_file)
        print(add_rep + csv_file)
        convert_excel_to_csv(add_rep + excel_file, add_rep + csv_file)
