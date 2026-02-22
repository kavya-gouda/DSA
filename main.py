ransomNote = "a", magazine = "b"
for i in ransomNote:
    if i in magazine:
        magazine = magazine.replace(i, "", 1)
    else:
        print(False)
        break