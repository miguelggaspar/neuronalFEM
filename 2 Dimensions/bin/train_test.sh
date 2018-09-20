echo "first argument (Number of time points): $1"
echo "second argument (Total time): $2"
echo "third argument (Emax value): $3"
echo "fourth argument (Emax value): $4"
echo "fifth argument (Emax value): $5"


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
python3 ../testmodel/src/test_model.py $1 $2 $3 $4 $5
# Making graphs for debugging
python3 ../testmodel/src/compare.py $3 $4 $5
