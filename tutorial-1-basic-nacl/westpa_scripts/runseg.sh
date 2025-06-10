#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

echo "PORT NUMBER: $WEST_SEG_PORT"

PORT=$((WEST_SEG_PORT +10000))

ln -sv $WEST_SIM_ROOT/common_files/bstate.gro .
ln -sv $WEST_SIM_ROOT/common_files/topol.top nacl.top
ln -sv $WEST_SIM_ROOT/common_files/tip3p_ionsjc2008.ff .
# ln -sv $WEST_SIM_ROOT/common_files/template.tpr .

sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.mdp > md.mdp

# Run the GROMACS preprocessor 
$GMX grompp -f md.mdp -c parent.gro -e parent.edr -p nacl.top \
  -t parent.trr -o seg.tpr -po md_out.mdp

# Propagate the segment using gmx mdrun
$GMX mdrun -s   seg.tpr -o seg.trr -c  seg.gro -e seg.edr \
  -cpo seg.cpt -g seg.log -nt 1 -imdwait -imdport $PORT &

#Calculate pcoord with MDAnalysis
python $WEST_SIM_ROOT/common_files/get_distance_streaming.py $PORT 
cat dist.dat > $WEST_PCOORD_RETURN


cp seg.gro $WEST_TRAJECTORY_RETURN
cp seg.trr $WEST_TRAJECTORY_RETURN
cp seg.edr $WEST_TRAJECTORY_RETURN

cp seg.gro $WEST_RESTART_RETURN/parent.gro
cp seg.trr $WEST_RESTART_RETURN/parent.trr
cp seg.edr $WEST_RESTART_RETURN/parent.edr

cp seg.log $WEST_LOG_RETURN

# Clean up all the files that we don't need to save.
rm -f dist.dat md.mdp md_out.mdp nacl.top  parent.trr seg.cpt seg.pdb seg.tpr parent.edr

