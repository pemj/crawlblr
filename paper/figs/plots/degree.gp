set xlabel "reblogs/total posts"
set ylabel "users"
set boxwidth 0.5
set style fill solid
plot "../../../results/degree.dat" using 2:1:xtic(2) with boxes notitle
