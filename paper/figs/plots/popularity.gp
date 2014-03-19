set xlabel "post type"
set xlabel font "Times-Roman, 11"
set ylabel "popularity"
set boxwidth 0.5
set logscale y
set ylabel font "Times-Roman, 11"
set xtics font "Times-Roman, 11"
set ytics font "Times-Roman, 11"
set xtics rotate by -25
set style fill solid
plot "../../../results/popularity.dat" using 2:xtic(1) with boxes notitle
