import copy
import zlib

crc32_table_polyrev=[]
poly_rev=0xedb88320
ini5_table=[]
def main():
    for byte in range(256):
        operator = copy.copy(byte)
        for bit in range(8):
            if (operator & 0x1) != 0:
                operator >>= 1
                operator ^= poly_rev
            else:
                operator >>= 1
        crc32_table_polyrev.append(operator)
    for i in range(1000000):
        ini5_table.append(crc32_polyrev(str(i)))
    to_print = list(map(hex, ini5_table))

def crc32_polyrev(line):
    var=0xffffffff
    for ch in line:
        operator=ord(ch)
        operator=(operator^var)&0xff
        var=crc32_table_polyrev[operator]^(var>>8)
    return var

def finder(num):
    for i in range(256):
        if num==(crc32_table_polyrev[i]>>24):
            return crc32_table_polyrev[i],i

def matcher(num,exceptions):
    for i in range(1000000):
        a=[(ini5_table[i]>>28)&0xf,(ini5_table[i]>>20)&0xf,(ini5_table[i]>>12)&0xf,(ini5_table[i]>>4)&0xf]
        b=[(num>>28)&0xf,(num>>20)&0xf,(num>>12)&0xf,(num>>4)&0xf]
        if a==b:
        #if ((ini5_table[i]>>28)==(num>>28))&(((ini5_table[i]>>20)&0xf)==((num>>20)&0xf))&(((ini5_table[i]>>12)&0xf)==((num>>12)&0xf))&(((ini5_table[i]>>4)&0xf)==((num>>4)&0xf)):
            if ini5_table[i] not in exceptions:
                return ini5_table[i],str(i)

def crc_any(ini,l4_set):
    var=copy.copy(ini)
    num_set=[]
    for each in l4_set:
        index=copy.copy(each)
        order=index^(var&0xff)
        if order>0x39 or order<0x30:
            return -1
        num=chr(order)
        num_set.append(num)
        var=crc32_table_polyrev[index]^(var>>8)
    numline=''.join(num_set)
    return numline

def crackl4(line):
    ori=''.join(['0x',line])
    ori=int(ori,16)
    ori^=0xffffffff
    var=copy.copy(ori)
    last4=[0 for i in range(4)]
    for i in range(4):
        f2=var>>24
        table_var,table_index=finder(f2)
        #print(hex(table_index),hex(table_var))
        #查表找到对应值和对应序号
        var6=var^table_var
        var=var6<<8
        #将16进制数6位扩展到8位
        adder=table_index^0x30
        var^=adder
        var=((var>>4)<<4)
        last4[3-i]=table_index
        #为16进制数添加倒数第二位
        #if (hex(var)[2:10].count('f'))>3:
        #    return last4,-1
    exceptions=[]
    l4_index=-1
    while l4_index==-1:
        f6,f6_index=matcher(var,exceptions)
        #print(hex(f6),f6_index)
        l4_index=crc_any(f6,last4)
        if l4_index==-1:
            exceptions.append(f6)
    return (''.join([f6_index,l4_index])),1
