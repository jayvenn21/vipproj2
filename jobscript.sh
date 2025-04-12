#!/bin/bash
#SBATCH -N1 -n10                         
#SBATCH --mem-per-cpu=16G               
#SBATCH -t15                             
#SBATCH -oReport-%j.out   

TASK=$1
INPUT_FILE=$2
OUTPUT_FILE=$3

echo "Running $TASK..."
case $TASK in
  ("Summarize")
    srun python summarize.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"
    ;;
  ("Translate")
    srun python translate.py --config "$INPUT_FILE"
    ;;
  ("Answer Question")
    srun python qa.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"
    ;;
  ("Classify")
    srun python classify.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"
    ;;
  (*)
    echo "Unknown task: $TASK"
    exit 1
    ;;
esac