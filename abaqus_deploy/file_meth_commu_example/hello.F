program Hello
  real(8):: Ei11, Ei22, Ei12, R, S, X11, X22, X12, p
  real(8):: dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
  print *,'Fortran program running'
C get values to send
  Ei11 = -0.0002
  Ei22 = 0.0001
  Ei12 = 0
  R = 53
  S = 50
  X11 = -0.04
  X22 = 0.015
  X12 = 0
  p = 0.006
C
  print *,' Fortran : saving state to txt file'
  open(100, file='state.txt')
  write (100,*)Ei11,',',Ei22,',',Ei12,',',R,',',S,',',X11,',',X22,',',X12,',',p
C close send file
  close(100)
C Execute python program to obtain
  print *,'Fortran: Executing python program'
  call system("python3 main.py")
C Open state into send file
  print *,' Fortran : loading state from txt file'
  open(101, file='derivatives.txt')
  read (101,*) dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
C close send file
  close(101)
  print *,'Fortran: Cat state file'
  call system("cat state.txt")
  print *,'Fortran: Cat derivatives file'
  call system("cat derivatives.txt")
  print *,'Fortran program ended'
end
