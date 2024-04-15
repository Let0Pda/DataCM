#!/bin/sh
if [ -f aclImdb_v1.tar.gz ]; then
    echo "aclImdb_v1.tar.gz already exists"
else
    wget http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
fi

tar -xzf aclImdb_v1.tar.gz
sed -i -e 's/"//g' -e 's/<br \/>//g' -e 's/\t//g' -e 's/\n//g' -e 's/;//g' -e '$s/$/;/' -e '$a\' aclImdb/train/pos/*.txt
cat aclImdb/train/pos/*.txt > positive.txt
sed -i -e 's/"//g' -e 's/<br \/>//g' -e 's/\t//g' -e 's/\n//g' -e 's/;//g' -e '$s/$/;/' -e '$a\' aclImdb/train/neg/*.txt
cat aclImdb/train/neg/*.txt > negative.txt
