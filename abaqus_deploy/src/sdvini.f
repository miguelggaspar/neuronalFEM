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
