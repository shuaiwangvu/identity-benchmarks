# FILES="./*.ttl.*"
# for f in $FILES
# do
# 	# rdf2hdt $f $f.hdt
# 	echo $f
# 	bzip2 -d $f
# done

# next, convert all the turtle files to hdt files
FILES="./*.ttl"
for f in $FILES
do
	# hdt2rdf $f $f.nt
	rdf2hdt $f $f.hdt
done


# and then convert the hdt files to nt files.

FILES="./*.hdt"
for f in $FILES
do
	hdt2rdf $f $f.nt
	# rdf2hdt $f $f.hdt
done

#
cat *.nt > dbpedia.nt
#
rdf2hdt bro.nt bro.hdt
