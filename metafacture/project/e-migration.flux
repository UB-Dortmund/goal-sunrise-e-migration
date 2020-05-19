default sourceFile = FLUX_DIR + "input.xml";
default targetFile = "output.xml";

default id_map = FLUX_DIR + "id.map.tsv";

default morphfile1 = FLUX_DIR + "morph1.xml";

sourceFile|
open-file|
decode-xml|
handle-marcxml|
morph(morphfile1, *)|
encode-marcxml|
write(targetFile);
