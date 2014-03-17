set xlabel "reblogs/total posts"
set xlabel font "Times-Roman, 12"
set ylabel "users"
set ylabel font "Times-Roman, 12"
set xtics font "Times-Roman, 12"
set ytics font "Times-Roman, 12"
set boxwidth 0.5
set style fill solid
set xtics rotate by -25
plot "../../../results/degree.dat" using 1:xtic(2) with boxes notitle
