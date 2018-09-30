rm build/*
for sourceName in basic_square_wave bias default delay; do
  gcc plugins/$sourceName.c -I ./lib -fPIC -flat_namespace -shared -undefined dynamic_lookup -o build/$sourceName.dylib
done