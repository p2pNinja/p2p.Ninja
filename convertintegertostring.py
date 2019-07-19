def str2int(s):
    chars = "".join(str(n) for n in range(10)) + "bcdfghjklmpqrvwxyz"
    # we have saved the five vowels and TNS for costumization
    i = 0
    for c in reversed(s):
        if c in chars:
            i *= len(chars)
            i += chars.index(c)
        else:
            pass
    return i

def int2str(i):
    chars = "".join(str(n) for n in range(10)) + "bcdfghjklmpqrvwxyz"
    # we have saved the five vowels and TNS for costumization
    s = ""
    while i:
        s += chars[i % len(chars)]
        i //= len(chars)
    return s

print (int2str(3233))
input ('hit any key to exit')
