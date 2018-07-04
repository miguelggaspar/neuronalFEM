echo "first argument (Input file): $1"
echo "second argument (User subroutine): $2"
# Run elas_axidisp job with elastic user defined subroutine
/usr/simulia/abaqus/Commands/abaqus job=$1 user=$2 int

# Dump pickl for post processing
#/usr/simulia/abaqus/Commands/abaqus viewer noGUI=post_process_abq

# Post process data
#python post_process.py

# Post process
/usr/simulia/abaqus/Commands/abaqus viewer noGUI=abaqus_read_odb -- $1

# Move png generated files to results folder
mv *.png results/
# Delete all files except .inp, .f, .sh and .py files
rm $(ls -1 | grep -v '.*\.py' | grep -v '.*\.f' | grep -v '.*\.inp' | grep -v '.*\.odb' | grep -v '.*\.sh' | grep -v '.*\.bkp')
rm *.fil
