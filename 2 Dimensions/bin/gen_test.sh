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


################################################################
####                  TEST MODEL                            ####
################################################################
# Delete previous tests
rm -rf ../testmodel/results/*.csv
rm -rf ../testmodel/graphs/xx/*.png ../testmodel/graphs/yy/*.png ../testmodel/graphs/xy/*.png
# Test model
python3 ../testmodel/test_model.py $1 $2 $3 $4 $5
# Making graphs for debugging
python3 ../testmodel/compare.py $3 $4 $5
