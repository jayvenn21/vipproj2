#!/bin/bash
#SBATCH -N1 -n1                         
#SBATCH --mem-per-cpu=16G               
#SBATCH -t15                             


TASK=$1
INPUT_FILE=$2
OUTPUT_FILE=$3

echo "Running $TASK..."
case $TASK in
  ("Summarize")
    srun python ~/vipproj2/milestone_2_2/hpc_summarize.py 
    ;;
  ("Translate")
    srun python ~/vipproj2/milestone_2_2/hpc_translate.py 
    ;;
  ("'Answer Question'")
    srun python ~/vipproj2/milestone_2_2/hpc_qa.py 
    ;;
  ("Classify")
    srun python ~/vipproj2/milestone_2_2/hpc_classify.py 
    ;;
  (*)
    echo "Unknown task: $TASK"
    exit 1
    ;;
esac