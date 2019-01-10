echo "first argument (Number of time points): $1"
echo "second argument (Total time): $2"
echo "third argument (Emax value): $3"
echo "fourth argument (Emax value): $4"
echo "fifth argument (Emax value): $5"
echo "sixth argument (Emax value): $6"
echo "seventh argument (Emax value): $7"

################################################################
####                  TRAINING                              ####
################################################################
# Train the mlp regressor
python3 ../train/src/train.py $1


################################################################
####                  TEST MODEL                            ####
################################################################
# Delete previous tests
# rm -rf ../testmodel/results/*.csv
rm -rf ../testmodel/graphs/xx/*.png ../testmodel/graphs/yy/*.png ../testmodel/graphs/xy/*.png
# Test model
python3 ../testmodel/src/test_model.py $1 $2 $3 $4 $5 $6 $7 $8 $9 $10 $11 $12 $13 $14 $15 $16 $17 $18 $19 $20 $21 $22 $23 $24
# Making graphs for debugging
python3 ../testmodel/src/compare.py $3 $4 $5 $6 $7 $8 $9 $10 $11 $12 $13 $14 $15 $16 $17 $18 $19 $20 $21 $22 $23 $24
