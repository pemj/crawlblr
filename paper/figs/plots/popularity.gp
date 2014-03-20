set style data histogram
set style histogram gap 1
set xrange [.5:9.5]
set xlabel "post type"
set xlabel font "Times-Roman, 11"
set ylabel "popularity"
set boxwidth .9 relative
set logscale y
set ylabel font "Times-Roman, 11"
set xtics font "Times-Roman, 11"
set ytics font "Times-Roman, 11"
set xtics rotate by -25
set xtics offset -3
set style fill transparent solid .7 noborder
plot "../../../results/popularity.dat" using 2 notitle, '' using 3:xticlabels(1) notitle


