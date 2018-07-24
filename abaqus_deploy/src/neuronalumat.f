*****************************************************************************
**  UMAT FOR ABAQUS/STANDARD INCORPORATING ELASTIC BEHAVIOUR  FOR PLANE    **
**  STRAIN AND AXI-SYMMETRIC ELEMENTS.                                     **
*****************************************************************************
*****************************************************************************
**
**
**
*USER SUBROUTINE
      SUBROUTINE UMAT(STRESS,STATEV,DDSDDE,SSE,SPD,SCD,
     1 RPL,DDSDDT,DRPLDE,DRPLDT,
     2 STRAN,DSTRAN,TIME,DTIME,TEMP,DTEMP,PREDEF,DPRED,CMNAME,
     3 NDI,NSHR,NTENS,NSTATV,PROPS,NPROPS,COORDS,DROT,PNEWDT,
     4 CELENT,DFGRD0,DFGRD1,NOEL,NPT,LAYER,KSPT,KSTEP,KINC)
C
      INCLUDE 'ABA_PARAM.INC'
C
      CHARACTER*80 CMNAME
C
C
      DIMENSION STRESS(NTENS),STATEV(NSTATV),
     1 DDSDDE(NTENS,NTENS),DDSDDT(NTENS),DRPLDE(NTENS),
     2 STRAN(NTENS),DSTRAN(NTENS),TIME(2),DTIME(1),PREDEF(1),DPRED(1),
     3 PROPS(NPROPS),COORDS(3),DROT(3,3),DFGRD0(3,3),DFGRD1(3,3)
C
C
      PARAMETER (M=3,N=3,ID=3,ZERO=0.D0,ONE=1.D0,TWO=2.D0,THREE=3.D0,
     +          SIX=6.D0, NINE=9.D0, TOLER=0.D-6)
C
      DIMENSION DSTRESS(4), DDS(4,4), SDEV(3), XDEV(3)
      real(8) dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
C      real(8) Ei11, Ei22, Ei12, R, X11, X22, X12, p
C
C
C
      write(*,*)"inside UMAT"
C
C
C
C--------------------------------------------------------------------
C
C     SPECIFY MATERIAL PROPERTIES
C Things to be updated: STRESS, DDSDDE, STATEV,
C
C
      v = PROPS(1)
      E = PROPS(2)
      Ei11 = STATEV(1)
      Ei22 = STATEV(2)
      Ei12 = STATEV(3)
      X11 = STATEV(4)
      X22 = STATEV(5)
      X12 = STATEV(6)
      R = STATEV(7)
      p = STATEV(8)
C
C change STRAN to DSTRAN
C    CALCULATE STRESS MATRIX
      DDSDDE(1,1) = E/(1-v**2)
      DDSDDE(1,2) = (E*v)/(1-v**2)
      DDSDDE(1,3) = 0
      DDSDDE(2,1) = (E*v)/(1-v**2)
      DDSDDE(2,2) = E/(1-v**2)
      DDSDDE(2,3) = 0
      DDSDDE(3,1) = 0
      DDSDDE(3,2) = 0
      DDSDDE(3,3) = ((1-v)*E)/(2*(1-v**2))
C
C
      STRESS(1) = (E/(1-v**2))*(DSTRAN(1)-STATEV(1)) +
     +            (v*E)/(1-v**2)*(DSTRAN(2)-STATEV(2))
      STRESS(2) = ((v*E)/(1-v**2))*(DSTRAN(1)-STATEV(1))+
     +            (E/(1-v**2))*(DSTRAN(2)-STATEV(2))
      STRESS(3) = ((1-v)/2)*(E/(1-v**2))*(DSTRAN(3)-STATEV(3))
C
C      write(*,*)"Stress Tensor",STRESS(1),STRESS(2),STRESS(3)
C      write(*,*)"DStran Tensor",DSTRAN(1),DSTRAN(2),DSTRAN(3)
C      write(*,*)"Stran Tensor",STRAN(1),STRAN(2),STRAN(3)
      open(unit=16, file='/home/miguel/state.txt')
      WRITE(16,*)Ei11,',',Ei22,',',Ei12,',',R,
     +           ',',STRESS(1),',',STRESS(2),',',STRESS(3),
     +            ',',X11,',',X22,',',X12,',',p,
     +            ',',DSTRAN(1),',',DSTRAN(2),',',DSTRAN(3)
C
C      WRITE(*,*)Ei11,',',Ei22,',',Ei12,',',R,
C     +           ',',STRESS(1),',',STRESS(2),',',STRESS(3),
C     +            ',',X11,',',X22,',',X12,',',p
C        Print *, STRESS(1)
C     print *, "Exit status of external_prog.exe was ", i
      CLOSE(16)
      call system("/usr/bin/python /home/miguel/call_neuronalfem.py")
      open(unit=17, file='/home/miguel/derivatives.txt')
      read (17,*) dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
      CLOSE(17)
C
      open(unit=18, file='/home/miguel/state1.txt')
      WRITE(18,*)dEi11,',',dEi22,',',dEi12,',',dR,
     +            ',',dX11,',',dX22,',',dX12,
     +            ',',dp
      CLOSE(18)
C
      WRITE(*,*)STATEV(1),',',STATEV(2)
      STATEV(1) = Ei11 + dEi11*DTIME(1)
      STATEV(2) = Ei22 + dEi22*DTIME(1)
      STATEV(3) = Ei12 + dEi12*DTIME(1)
      STATEV(4) = X11 + dX11*DTIME(1)
      STATEV(5) = X22 + dX22*DTIME(1)
      STATEV(6) = X12 + dX12*DTIME(1)
      STATEV(7) = R + dR*DTIME(1)
      STATEV(8) = p + dp*DTIME(1)


      WRITE(*,*)STATEV(1),',',STATEV(2)
C
      write(*,*)"Outside UMAT"
      RETURN
      END
**
**
**
**
********************************************
**    USDFLD TO UPDATE STATE VARIABLES     *
********************************************
*USER SUBROUTINE
      SUBROUTINE USDFLD(FIELD, STATEV, PNEWDT, DIRECT, T,
     1 CELENT, TIME, DTIME, CMNAME, ORNAME, NFIELD,
     2 NSTATV, NOEL, NPT, LAYER, KSPT, KSTEP, KINC, NDI,
     3 NSHR, COORD, JMAC, JMATYP, MATLAYO, LACCFLA)
C
      INCLUDE 'ABA_PARAM.INC'
C
      CHARACTER*80 CMNAME,ORNAME
      CHARACTER*8 FLGRAY(15)
      DIMENSION FIELD(NFIELD), STATEV(NSTATV), DIRECT(3, 3),
     1 T(3, 3), TIME(2), COORD(*), JMAC(*), JMATYP(*)
      DIMENSION ARRAY(15), JARRAY(15), DTIME(1)
C
      real(8) dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
C
      open(unit=17, file='/home/miguel/derivatives.txt')
      read (17,*) dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
      CLOSE(17)
C
C
      write(*,*)"inside USDFLD"
      WRITE(*,*)STATEV(1)
      STATEV(1) = STATEV(1) + dEi11*DTIME(1)
      WRITE(*,*)STATEV(1)
      write(*,*)"outisde USDFLD"
      STATEV(2) = STATEV(2) + dEi22*DTIME(1)
      STATEV(3) = STATEV(3) + dEi12*DTIME(1)
      STATEV(4) = STATEV(4) + dX11*DTIME(1)
      STATEV(5) = STATEV(5) + dX22*DTIME(1)
      STATEV(6) = STATEV(6) + dX12*DTIME(1)
      STATEV(7) = STATEV(7) + dR*DTIME(1)
      STATEV(8) = STATEV(8) + dp*DTIME(1)
      RETURN
      END
