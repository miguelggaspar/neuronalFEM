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
#rm -rf ../dataset/results/*.csv
#rm -rf ../dataset/graphs/xx/*.png ../dataset/graphs/yy/*.png ../dataset/graphs/xy/*.png
# Generate dataset based on a defined viscoplasticity model
python3 ../dataset/src/viscoplasticity_model.py $1 $2 $3 $4 $5 $6 $7 $8 $9 $10 $11 $12 $13 $14 $15 $16 $17 $18 $19 $20 $21 $22 $23 $24
# Make graphs for debugging
#python3 ../dataset/src/load.py $3 $4 $5 $6 $7 $8 $9 $10 $11 $12 $13 $14 $15 $16 $17 $18 $19 $20 $21 $22 $23 $24
# Merge all trial's data to one .csv file
# python3 ../dataset/src/merge_csv.py $3 $4 $5 $6 $7 $8 $9 $10 $11 $12 $13 $14 $15 $16 $17 $18 $19 $20 $21 $22 $23 $24
