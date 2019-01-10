*****************************************************************************
**  UMAT FOR ABAQUS/STANDARD INCORPORATING PREDICTIVE MECHANICAL BEHAVIOUR **
**  BY NEURAL NETWORKS FOR PLANE-STRESS                                    **
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
      real(8) dEvp11, dEvp22, dEvp12, dR, dX11, dX22, dX12, dp
C
C     LOAD MATERIAL PROPERTIES AND STATE VARIABLES
C
      v = PROPS(1)
      E = PROPS(2)
      Evp11 = STATEV(1)
      Evp22 = STATEV(2)
      Evp12 = STATEV(3)
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
C     ASSIGN STRESS TENSOR TO LOCAL VARIABLES
C
      S11 = STRESS(1)
      S22 = STRESS(2)
      S12 = STRESS(3)
C
C     ASK FOR THE DERIVATIVES
C
      a = get_derivatives(Evp11, Evp22, Evp12, R, S11, S22,
     + S12, X11, X22, X12, p)
C
C     READ THE DERIVATIVES
C
      open(unit=17, file='/home/miguel/predictions.txt')
      read (17,*) dEvp11, dEvp12, dEvp22, dR, dX11, dX12, dX22, dp
      CLOSE(17)
C
C     TRANSFORM VISCOPLASTIC STRAIN RATE INTO INCREMENT
C
      Evp11_inc = dEvp11 * DTIME(1)
      Evp22_inc = dEvp22 * DTIME(1)
      Evp12_inc = dEvp12 * DTIME(1)
C
C     UPDATE STRESS
C
      STRESS(1) = S11 + DDSDDE(1,1)*(DSTRAN(1)-Evp11_inc)+
     +            DDSDDE(1,2)*(DSTRAN(2)-Evp22_inc)
      STRESS(2) = S22 + DDSDDE(2,1)*(DSTRAN(1)-Evp11_inc)+
     +            DDSDDE(2,2)*(DSTRAN(2)-Evp22_inc)
      STRESS(3) = S12 + DDSDDE(3,3)*(DSTRAN(3)-Evp12_inc)
C
C     UPDATE STATE VARIABLES
C
      STATEV(1) = Evp11 + dEvp11*DTIME(1)
      STATEV(2) = Evp22 + dEvp22*DTIME(1)
      STATEV(3) = Evp12 + dEvp12*DTIME(1)
      STATEV(4) = X11 + dX11*DTIME(1)
      STATEV(5) = X22 + dX22*DTIME(1)
      STATEV(6) = X12 + dX12*DTIME(1)
      STATEV(7) = R + dR*DTIME(1)
      STATEV(8) = p + dp*DTIME(1)
      RETURN
      END
**
**************************************************************************
**                       UTILITY    FUNCTIONS                           **
**************************************************************************
**
**
**************************************************************************
**         PREDICT STATE DERIVATIVES GIVEN A CERTAIN STATE              **
**************************************************************************
      real(8) function  get_derivatives(Evp11, Evp22, Evp12, R, S11, S22,
     1 S12, X11, X22, X12, p)
C
      real(8) Evp11, Evp22, Evp12, R, X11, X22, X12, p, S11, S22, S12
C
C     WRITE S,Evp,X TENSORS p AND R TO features.txt FILE
C
      open(unit=16, file='/home/miguel/features.txt')
      WRITE(16,*)Evp11,',',Evp12,',',Evp22,',',R,
     +           ',',S11,',',S12,',',S22,
     +            ',',X11,',',X12,',',X22,',',p
      CLOSE(16)
C
C     CALL MACHINE LEARNING MODEL TO MAKE PREDICTIONS
C     THEN WAIT UNTIL IT FINISH EXECUTION
C
      call system("/usr/bin/python /home/miguel/call_neuronalfem.py")
      return
      end
*****************************************************************************
**  SDVINI FOR ABAQUS/STANDARD                                             **
**                                                                         **
*****************************************************************************
*****************************************************************************
**
**
**
*USER SUBROUTINE
      SUBROUTINE SDVINI(STATEV,COORDS,NSTATV,NCRDS,NOEL,NPT,
     1 LAYER,KSPT)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION STATEV(NSTATV),COORDS(NCRDS)
C
C     ASSIGN INITIAL CONDITIONS TO STATE VARIABLES
C
      STATEV(1) = 0.
      STATEV(2) = 0.
      STATEV(3) = 0.
      STATEV(4) = 0.
      STATEV(5) = 0.
      STATEV(6) = 0.
      STATEV(7) = 50.
      STATEV(8) = 0.
      RETURN
      END
