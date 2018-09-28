with open("/Users/manikant/Desktop/filesofdifferentsizes/2000mb.txt", "wb") as out:
    out.truncate(2000 *1024 *1024)
