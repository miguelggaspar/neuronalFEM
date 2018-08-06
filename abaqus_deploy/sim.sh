echo "first argument (Input file): $1"
echo "second argument (User subroutine): $2"

# Prepare initial conditios for USDFLD subroutine
cp src/statev_initial_cond.txt ~/statev.txt
cp src/stat_initial_cond.txt ~/state.txt
cp src/deriv_initial_cond.txt ~/derivatives.txt

# Run elas_axidisp job with elastic user defined subroutine
/usr/simulia/abaqus/Commands/abaqus job=$1 user=src/$2 interactive

# Dump pickl for post processing
#/usr/simulia/abaqus/Commands/abaqus viewer noGUI=post_process_abq

# Post process data
#python post_process.py

# Post process
#/usr/simulia/abaqus/Commands/abaqus viewer noGUI=abaqus_read_odb -- $1

# Move png generated files to results folder
#mv *.png results/
mv derivatives.txt der_$1.txt
mv state.txt stat_$1.txt
# Delete all files except .inp, .f, .sh and .py files
# rm $(ls -1 | grep -v '.*\.py' | grep -v '.*\.f' | grep -v '.*\.inp' |
#   grep -v '.*\.odb' | grep -v '.*\.sh' | grep -v '.*\.bkp' | grep -v '.*\.txt')
# rm *.fil
