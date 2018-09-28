from fsplit.filesplit import FileSplit
import os
from datetime import datetime
import time
import hashlib
from dbhandler import * 


kilobytes = 1024
megabytes = kilobytes * 1024
chunksize = int(5 * megabytes)                   # default: roughly a floppy
readsize = 1024
blob_sequence = 0

def split(fromfile, todir="/Users/manikant/Documents/blob_storage/local/blobs", chunksize=chunksize, blob_sequence = blob_sequence): 
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        for fname in os.listdir(todir):            # delete any existing files
            os.remove(os.path.join(todir, fname)) 
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        md5_chunk = md5(chunk)
        partnum  = partnum+1
        blob_sequence+=1
        blob_id = getblobIdMd5(md5_chunk)
        if(blob_id != ""):
            insertFileBlob(fromfile, blob_sequence, blob_id)
            insertBlobMd5("", md5_chunk)
        else:       
            filename = os.path.join(todir, ('part%04d' % blob_sequence))
            fileobj  = open(filename, 'wb')
            fileobj.write(chunk)
            fileobj.close()                            # or simply open(  ).write(  )
            insertBlobMd5(filename, md5_chunk)
            blob_id = getblobIdMd5(md5_chunk)
            insertFileBlob(fromfile, blob_sequence, blob_id)
            insertBlobMd5("", md5_chunk)

    input.close()
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum

def join(fromdir, tofile):
    output = open(tofile, 'wb')
    parts  = os.listdir(fromdir)
    parts.sort(  )
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read(readsize)
            if not filebytes: break
            output.write(filebytes)
        fileobj.close(  )
    output.close(  )

def md5(chunk):
    hash_md5 = hashlib.md5()
    hash_md5.update(chunk)
    return hash_md5.hexdigest()

# split('2000mb.txt', 'blobs')
# join('blobs','2000mb_join.txt')
# print(md5('2000mb.txt'))


def uploadfile(filepath):
    split(filepath)

uploadfile("/Users/manikant/Documents/blob_storage/400mb_component_dcxfile.dcxalbum")