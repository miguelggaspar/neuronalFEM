echo "first argument (Input file): $1"
echo "second argument (User subroutine): $2"

# Prepare initial conditios for USDFLD subroutine
cp initial_conditions/features.txt ~/features.txt
cp initial_conditions/predictions.txt ~/predictions.txt
cp src/call_neuronalfem.py ~/call_neuronalfem.py
# Run elas_axidisp job with elastic user defined subroutine
/usr/simulia/abaqus/Commands/abaqus job=$1 user=src/$2 interactive

# Delete all files except .inp, .f, .sh and .py files
 rm $(ls -1 | grep -v '.*\.py' | grep -v '.*\.f' | grep -v '.*\.inp' |
   grep -v '.*\.odb' | grep -v '.*\.sh' | grep -v '.*\.bkp' | grep -v '.*\.txt')
 rm *.fil
