echo "first argument (Number of time points): $1"
echo "second argument (Total time): $2"
echo "third argument (Emax value): $3"
echo "fourth argument (Emax value): $4"
echo "fifth argument (Emax value): $5"


################################################################
####                  DATASET                               ####
################################################################
# Delete previous data
rm -rf ../dataset/results/*.csv
rm -rf ../dataset/graphs/xx/*.png ../dataset/graphs/yy/*.png ../dataset/graphs/xy/*.png
# Generate dataset based on a defined viscoplasticity model
python ../dataset/viscoplasticity_model.py $1 $2 $3 $4 $5
# Make graphs for debugging
#python ../dataset/load.py $3 $4 $5
# Merge all trial's data to one .csv file
python ../dataset/merge_csv.py $3 $4 $5


################################################################
####                  TRAINING                              ####
################################################################
# Train the mlp regressor
python3 ../train/train.py
