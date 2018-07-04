! program reader
!  integer :: a(1024), i, result, nlines , j
!  double precision :: test
program read
  real(8):: Ei11, Ei22, Ei12, R, S, X11, X22, X12, p
  real(8):: dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
  ! real(8) x
  ! double precision y, z
  ! x = 0.1111111111
  ! y = 1.1
  ! z = 1.1D0
  ! print *, "x =", x, " , y =", y, " , z =", z
  print *,'Fortran program running'
  !get values to send
  Ei11 = -0.0002 !Ei11
  Ei22 = 0.0001  !Ei22
  Ei12 = 0       !Ei12
  R = 53         !R
  S = 50         !S
  X11 = -0.04    !X11
  X22 = 0.015    !X22
  X12 = 0        !X12
  p = 0.006      !p

  print *,' Fortran : saving state to txt file'
  open(100, file='state.txt')
  write (100,*)Ei11,',',Ei22,',',Ei12,',',R,',',S,',',X11,',',X22,',',X12,',',p
  !close send file
  close(100)
  !Execute python program to obtain
  print *,'Fortran: Executing python program'
  call system("python3 main.py")
  !Open state into send file
  print *,' Fortran : loading state from txt file'
  open(101, file='derivatives.txt')
  read (101,*) dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
  
  !close send file
  close(101)
  print *,'Fortran: Cat state file'
  call system("cat state.txt")
  print *,'Fortran: Cat derivatives file'
  call system("cat derivatives.txt")
  print *,'Fortran program ended'
end program
