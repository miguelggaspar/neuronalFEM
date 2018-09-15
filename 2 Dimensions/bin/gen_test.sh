# Generate dataset based on a defined viscoplasticity model
python ../dataset/viscoplasticity_model.py
# Make graphs for debugging
#python ../dataset/load.py
# Merge all trial's data to one .csv file
python ../dataset/merge_csv.py
# Testing model
python3 ../testmodel/test_model.py
# Making graphs for debugging
python3 ../testmodel/compare.py
