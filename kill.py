import polars as pl
import pandas as pd
from collections import defaultdict

def load_and_prepare_dataset(paths):
    headers = ["FIRSTNAME", "LASTNAME"]
    names_list = []
    
    for f in sorted(paths.glob("*.csv")):
        df = pl.read_csv(f, has_header=False, columns=[0, 1], new_columns=headers)
        names_list.append(df)
    
    names_df = pl.concat(names_list, how="vertical")
    names_df = names_df.drop_nulls()
    names_df = names_df.filter((names_df["FIRSTNAME"].str.len_chars() >= 3) & (names_df["LASTNAME"].str.len_chars() >= 3))
    
    return names_df

def process_alternative_names(name_df, similar_names_path, name_column):
    similar_names_df = pd.read_csv(similar_names_path, sep="\t")
    similar_names_map = defaultdict(list)
    
    for _, row in similar_names_df.iterrows():
        similar_names_map[row["name"]] = row["confirmed_variants"].split()
    
    processed_data = []
    count_alternatives = 0
    
    for name in name_df[name_column]:
        if name in similar_names_map:
            for alt_name in similar_names_map[name]:
                processed_data.append([name, alt_name])
            count_alternatives += len(similar_names_map[name])
        else:
            processed_data.append([name, name])
    
    print(f"Processed {len(name_df)} names, found {count_alternatives} alternative names.")
    
    processed_df = pd.DataFrame(processed_data, columns=["name1", "name2"])
    processed_df["co_occurrence"] = processed_df.groupby(["name1", "name2"]).transform("count")
    
    return processed_df

def save_processed_data(df, output_path):
    df.to_csv(output_path, sep="\t", index=False)

def main():
    from pathlib import Path
    
    dataset_path = Path("../nama_notebooks/Assets/name_dataset_csvs/data/")
    firstname_similar_names_path = "../data_new/givenname_similar_names.werelate.20210414.tsv"
    lastname_similar_names_path = "../data_new/surname_similar_names.werelate.20210414.tsv"
    
    names_df = load_and_prepare_dataset(dataset_path)
    
    givenname_df = process_alternative_names(names_df, firstname_similar_names_path, "FIRSTNAME")
    save_processed_data(givenname_df, "givenname.tsv")
    
    lastname_df = process_alternative_names(names_df, lastname_similar_names_path, "LASTNAME")
    save_processed_data(lastname_df, "lastname.tsv")
    
if __name__ == "__main__":
    main()
