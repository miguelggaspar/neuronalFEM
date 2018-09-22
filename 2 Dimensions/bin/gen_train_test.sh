echo "first argument (Number of time points): $1"
echo "second argument (Total time): $2"
echo "third argument (Emax value): $3"
echo "fourth argument (Emax value): $4"
echo "fifth argument (Emax value): $5"
echo "sixth argument (Emax value): $6"
echo "seventh argument (Emax value): $7"


################################################################
####                  DATASET                               ####
################################################################
# Delete previous data
rm -rf ../dataset/results/*.csv
rm -rf ../dataset/graphs/xx/*.png ../dataset/graphs/yy/*.png ../dataset/graphs/xy/*.png
# Generate dataset based on a defined viscoplasticity model
python ../dataset/src/viscoplasticity_model.py $1 $2 $3 $4 $5 $6 $7
# Make graphs for debugging
#python ../dataset/load.py $3 $4 $5
# Merge all trial's data to one .csv file
python ../dataset/src/merge_csv.py $3 $4 $5 $6 $7


################################################################
####                  TRAINING                              ####
################################################################
# Train the mlp regressor
python3 ../train/src/train.py


################################################################
####                  TEST MODEL                            ####
################################################################
# Delete previous tests
rm -rf ../testmodel/results/*.csv
rm -rf ../testmodel/graphs/xx/*.png ../testmodel/graphs/yy/*.png ../testmodel/graphs/xy/*.png
# Test model
python3 ../testmodel/src/test_model.py $1 $2 $3 $4 $5 $6 $7
# Making graphs for debugging
python3 ../testmodel/src/compare.py $3 $4 $5 $6 $7
