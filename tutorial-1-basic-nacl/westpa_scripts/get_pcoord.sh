#!/bin/bash
set -x
cd $WEST_SIM_ROOT
cd $WEST_STRUCT_DATA_REF
cat pcoord.init > $WEST_PCOORD_RETURN


cp $WEST_STRUCT_DATA_REF/bstate.gro $WEST_TRAJECTORY_RETURN/basis.gro
cp $WEST_STRUCT_DATA_REF/bstate.trr $WEST_TRAJECTORY_RETURN/basis.trr
cp $WEST_STRUCT_DATA_REF/bstate.edr $WEST_TRAJECTORY_RETURN/basis.edr


cp $WEST_STRUCT_DATA_REF/bstate.gro $WEST_RESTART_RETURN/parent.gro
cp $WEST_STRUCT_DATA_REF/bstate.trr $WEST_RESTART_RETURN/parent.trr
cp $WEST_STRUCT_DATA_REF/bstate.edr $WEST_RESTART_RETURN/parent.edr

