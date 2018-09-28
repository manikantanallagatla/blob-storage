import sqlite3


def getCountMd5(md5_sum):
    conn = sqlite3.connect('local/blobs_md5.db')
    # print("Opened database successfully")

    cursor = conn.execute("SELECT reference_count from BLOBS WHERE md5_sum = '" + md5_sum + "'")
    count_ans = 0
    for row in cursor:
        count_ans = row[0]

    # print("Operation done successfully")
    conn.close()
    return count_ans

def getblobIdMd5(md5_sum):
    blob_id = ""
    conn = sqlite3.connect('local/blobs_md5.db')
    # print("Opened database successfully")

    cursor = conn.execute("SELECT id from BLOBS WHERE md5_sum = '" + md5_sum + "'")
    for row in cursor:
        blob_id = row[0]

    # print("Operation done successfully")
    conn.close()
    return blob_id

def getCountBlobPath(blob_path):
    conn = sqlite3.connect('local/blobs_md5.db')
    # print("Opened database successfully")

    cursor = conn.execute("SELECT reference_count from BLOBS WHERE blob_path = '" + blob_path + "'")
    count_ans = 0
    for row in cursor:
        count_ans = row[0]

    # print("Operation done successfully")
    conn.close()
    return count_ans

def incrementCountMd5(md5_sum, count_ans):
    conn = sqlite3.connect('local/blobs_md5.db')
    # print("Opened database successfully")

    conn.execute("UPDATE BLOBS SET reference_count = '" + str(count_ans) + "' WHERE md5_sum = '" + md5_sum + "'")
    conn.commit()

    # print("Operation done successfully")
    conn.close()

def incrementCountBlobPath(blob_path, count_ans):
    conn = sqlite3.connect('local/blobs_md5.db')
    # print("Opened database successfully")

    conn.execute("UPDATE BLOBS SET reference_count = '" + str(count_ans) + "' WHERE blob_path = '" + blob_path + "'")
    conn.commit()

    # print("Operation done successfully")
    conn.close()

def insertBlobMd5(blob_path, md5_sum):
    count_ans = getCountMd5(md5_sum)
    if(count_ans > 0):
        incrementCountMd5(md5_sum, count_ans+1)
    else:
        conn = sqlite3.connect('local/blobs_md5.db')
        # print("Opened database successfully")

        command = "INSERT INTO BLOBS (blob_path, md5_sum, reference_count) VALUES ( '" + blob_path + "' , '" + md5_sum + "' , '0' )"
        # print(command)
        conn.execute(command)

        conn.commit()
        # print("Records created successfully")
        conn.close()

def insertFileBlob(filepath, blobsequencenumber, blob_id):
    conn = sqlite3.connect('local/blobs_md5.db')
    # print("Opened database successfully")

    command = "INSERT INTO FILE_BLOBS (filepath, blobsequencenumber, blobid) VALUES ( '" + filepath + "' , '" + str(blobsequencenumber) + "' , '" + str(blob_id) +"' )"
    # print(command)
    conn.execute(command)

    conn.commit()
    # print("Records created successfully")
    conn.close()

def deleteBlobPath(blob_path):
    count_ans = getCountBlobPath(blob_path)
    if(count_ans > 1):
        incrementCountBlobPath(blob_path, count_ans-1)
    else:
        conn = sqlite3.connect('local/blobs_md5.db')
        # print("Opened database successfully")

        command = "DELETE FROM BLOBS where blob_path = '" + blob_path + "'"
        # print(command)
        conn.execute(command)

        conn.commit()
        # print("Records created successfully")
        conn.close()

# insertBlobMd5('/Users/manikant/Documents/blob_storage/blobs/part0004', '5f363e0e58a95f06cbe9bbc662c5dfb6')
# deleteBlobPath('/Users/manikant/Documents/blob_storage/blobs/part0004')