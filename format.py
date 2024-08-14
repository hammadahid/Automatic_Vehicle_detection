#!/usr/bin/env python3

import pandas as pd


de = pd.read_csv('sample.csv')
grouped = de.groupby('car_id')

for name, group in grouped:
    max_row = group.loc[group[de.columns[2]].idxmax()]
    max_license_row = group.loc[group[de.columns[9]].idxmax()]

    max_value_license_plate = max_license_row[de.columns[8]]
    max_value_vehicle_type = max_row[de.columns[1]]

    # de.loc[group.index, de.columns[8]] = max_value_license_plate
    de.loc[group.index, de.columns[1]] = max_value_vehicle_type
    de.loc[group.index, de.columns[8]] = max_value_license_plate

de.to_csv('final_data.csv', index=False)


# df = pd.read_csv('sample_interpolated1.csv')

# grouped = df.groupby('car_id')

# # max_value = grouped['license_plate_bbox_score'].max()

# for name, group in grouped:
#     max_row = group.loc[group[df.columns[7]].idxmax()]
#     max_value_license_plate = max_row[df.columns[6]]
#     max_value_vehicle_type = max_row[df.columns[2]]

#     df.loc[group.index, df.columns[6]] = max_value_license_plate
#     df.loc[group.index, df.columns[2]] = max_value_vehicle_type

# df.to_csv('modified_sample.csv', index=False)
