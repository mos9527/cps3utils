def input_int(*a,**k):
    nVal = input(*a,**k)
    if str.isdecimal(nVal): nVal = int(nVal)
    else:
        nVal = int(nVal,16)
        print('...(Hexidecimal %x -> %d)' % (nVal,nVal))
    return nVal