# Delete all files except .inp, .f, .sh and .py files
rm $(ls -1 | grep -v '.*\.py' | grep -v '.*\.f' | grep -v '.*\.inp' |
   grep -v '.*\.odb' | grep -v '.*\.sh' | grep -v '.*\.bkp' | grep -v '.*\.txt')
rm *.fil
