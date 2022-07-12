import math


def convert_size(size_bytes):
   if size_bytes == 0:
       return 0
   p = math.pow(1024, 4)
   return size_bytes / p