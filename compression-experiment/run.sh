# git clone https://github.com/google/brotli + make
# git clone https://github.com/google/gipfeli + patch + make

refdata=../tools/refdata/

./brotli/bin/bro --input $refdata/Apache-2.0 > Apache-2.0.brotli
stat -c%s $refdata/Apache-2.0 Apache-2.0.brotli

./brotli/bin/bro --input $refdata/jolie.pdf > jolie.pdf.brotli
stat -c%s $refdata/jolie.pdf jolie.pdf.brotli

(cd gipfeli; ./gipfeli_test)
