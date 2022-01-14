k=1
start=`date +%s`

for filename in /home/nikhilanand_1921cs24/Souryadip/GDC/Downloads/*/*.svs
do

  if [ $k -gt 50 -a $k -lt  ]
   then
      id=$(basename "$filename" .svs)
  echo "Processing slide $k: $id"

  # Output filepath
  outpath="/home/nikhilanand_1921cs24/Souryadip/PyHIST/output"
  
  # Run PyHIST
  python pyhist.py \
    --save-patches \
	--method "otsu" \
	--format "jpg" \
    --content-threshold 0.4 \
    --patch-size 224 \
    --output-downsample 1 \
    --output "$outpath" \
    "$filename"
	
   fi

  k=$((k+1))
done

end=`date +%s`
runtime=$((end-start))
echo "Elapsed time: $runtime seconds"

