

rm -rf posts/*.html
sed -i 's/\r$//' posts/*

sed -i 's/\r$//' js/*

sed -i 's/\r$//' css/*

rm -rf _site
rm -rf _cache
mkdir _site/

cp -rfv js _site/
cp -rfv font _site/
cp -rfv images _site/
cp -rfv js _site/
cp -fv README.md _site/
