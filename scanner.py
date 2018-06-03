import re

tokens = {';','[',']',"ID",'NUM','int','void','(',')','{','}',"if","else","while","return","<","==","+","-","*",",","="}
f= open("testFile.txt", "r")
code = f.read()
words = code.split("\\s+")
tokenArray = []
for word in words:
    previusStr = tmpStr
    tmpStr = ""
    for letter in word:
        if letter in tokens:
            if tmpStr != "":
                if tmpStr in tokens:
                    tokenArray.append(tmpStr)
                    previusStr = tmpStr
                    tmpStr = ""

                # TODO: elif tmpStr is digit:
                    # TODO: free tmpStr
                # TODO: elif tmpStr is identifier:
                    # TODO: free tmpStr

            tokenArray.append(letter)

        else:
            if tmpStr in tokens:
                tokenArray.append(tmpStr)
                previusStr = tmpStr
                tmpStr = ""
                continue
            # TODO: elif tmpStr is digit:

            # TODO: elif tmpStr is identifier:

            else:
                tmpStr = tmpStr + letter


