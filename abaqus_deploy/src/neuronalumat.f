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
     3 PROPS(NPROPS),COORDS(3),DROT(3,3),DFGRD0(3,3),DFGRD1(3,3),
     4 KINC(1), KSTEP(1)
C
C
      PARAMETER (M=3,N=3,ID=3,ZERO=0.D0,ONE=1.D0,TWO=2.D0,THREE=3.D0,
     +          SIX=6.D0, NINE=9.D0, TOLER=0.D-6)
C
      DIMENSION DSTRESS(4), DDS(4,4), SDEV(3), XDEV(3)
      real(8) dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
      real(8) aux1, aux2, aux3, aux4, aux5, aux6, a
C
C     LOAD MATERIAL PROPERTIES AND STATE VARIABLES
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
C    CALCULATE ELASTIC STIFFNESS
c
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
C     CALCULATE STRESS BASED ON ELASTIC BEHAVIOR
C
      S11 = STRESS(1) + DDSDDE(1,1)*(DSTRAN(1))+
     +            DDSDDE(1,2)*(DSTRAN(2))
      S22 = STRESS(2) + DDSDDE(2,1)*(DSTRAN(1))+
     +            DDSDDE(2,2)*(DSTRAN(2))
      S12 = STRESS(3) + DDSDDE(3,3)*(DSTRAN(3))
C
C     FIRST PREDICTION
C
      a = get_derivatives(Ei11, Ei22, Ei12, R, S11, S22,
     + S12, X11, X22, X12, p, DSTRAN(1), DSTRAN(2), DSTRAN(3),
     + KINC, KSTEP, NOEL, NPT, KSPT)
C
C     LOOP TO GET CONVERGENCE
C
      DO K1 = 1, 5
        open(unit=17, file='/home/miguel/derivatives.txt')
        read (17,*) dEi11, dEi22, dEi12, dR, dX11, dX22, dX12, dp
        CLOSE(17)
        S11_temp = S11 + DDSDDE(1,1)*(DSTRAN(1)-dEi11)+
     +            DDSDDE(1,2)*(DSTRAN(2)-dEi22)
        S22_temp = S22 + DDSDDE(2,1)*(DSTRAN(1)-dEi11)+
     +            DDSDDE(2,2)*(DSTRAN(2)-dEi22)
        S12_temp = S12 + DDSDDE(3,3)*(DSTRAN(3)-dEi12)
C
        Ei11 = Ei11 + dEi11*DTIME(1)
        Ei22 = Ei22 + dEi22*DTIME(1)
        Ei12 = Ei12 + dEi12*DTIME(1)
        X11 = X11 + dX11*DTIME(1)
        X22 = X22 + dX22*DTIME(1)
        X12 = X12 + dX12*DTIME(1)
        R = R + dR*DTIME(1)
        p = p + dp*DTIME(1)
C
        a = get_derivatives(Ei11, Ei22, Ei12, R, S11_temp, S22_temp,
     + S12_temp, X11, X22, X12, p, DSTRAN(1), DSTRAN(2), DSTRAN(3),
     + KINC, KSTEP, NOEL, NPT, KSPT)
      END DO
C
C     UPDATE STRESS
C
      STRESS(1) = S11_temp
      STRESS(2) = S22_temp
      STRESS(3) = S12_temp
C
C     UPDATE STATE VARIABLES
C
      STATEV(1) = Ei11 + dEi11*DTIME(1)
      STATEV(2) = Ei22 + dEi22*DTIME(1)
      STATEV(3) = Ei12 + dEi12*DTIME(1)
      STATEV(4) = X11 + dX11*DTIME(1)
      STATEV(5) = X22 + dX22*DTIME(1)
      STATEV(6) = X12 + dX12*DTIME(1)
      STATEV(7) = R + dR*DTIME(1)
      STATEV(8) = p + dp*DTIME(1)
C
      RETURN
      END
**
***********************************************
**           UTILITY    FUNCTIONS             *
***********************************************
**
**
****************************************************
** PREDICT STATE DERIVATIVES GIVEN A CERTAIN STATE *
****************************************************
      real(8) function  get_derivatives(Ei11, Ei22, Ei12, R, S11, S22,
     1 S12, X11, X22, X12, p, DSTRAN1, DSTRAN2, DSTRAN3,
     2 KINC, KSTEP, NOEL, NPT, KSPT)
c
      real(8) Ei11, Ei22, Ei12, R, X11, X22, X12, p, S11, S22, S12,
     + DSTRAN1, DSTRAN2, DSTRAN3
      integer KINC(1), KSTEP(1), NOEL, NPT, KSPT
c
      open(unit=16, file='/home/miguel/state.txt')
      WRITE(16,*)Ei11,',',Ei22,',',Ei12,',',R,
     +           ',',S11,',',S22,',',S12,
     +            ',',X11,',',X22,',',X12,',',p,
     +            ',',DSTRAN1,',',DSTRAN2,',',DSTRAN3,
     +            ',',KINC,',',KSTEP,',',NOEL,',',NPT,',',KSPT
      CLOSE(16)

      call system("/usr/bin/python /home/miguel/call_neuronalfem.py")
      return
      end
