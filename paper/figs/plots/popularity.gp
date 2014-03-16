set xlabel "post type"
set ylabel "popularity"
set boxwidth 0.5
set logscale y
set xtics rotate by -25
set style fill solid
plot "../../../results/popularity.dat" using 2:xtic(1) with boxes notitle
