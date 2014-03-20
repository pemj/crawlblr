set style data histogram
set style histogram gap 1
set xrange [.5:10.5]
set xlabel "reblogs/total posts"
set xlabel font "Times-Roman, 12"
set format y "%g %%" 
set ylabel "users"
set ylabel font "Times-Roman, 12"
set xtics font "Times-Roman, 12"
set ytics font "Times-Roman, 12"
set boxwidth .9 relative
set style fill transparent solid .7 noborder
set xtics rotate by -25
set xtics offset -3
plot "../../../results/degree.dat" using 1:xtic(2) notitle
