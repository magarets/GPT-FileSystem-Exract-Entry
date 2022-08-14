"""
format : bytes
output : {GUID} {FileSystem Type} {실제 리얼 offset sector = byte} {사이즈 = byte}
"""
import binascii
import sys

SECTOR_SIZE = 512
ENTRY_SIZE = 128
SIGNATURE = 8
HEADER_SIZE = 4

FILENAME = "../gpt_128.dd"

"""
수정해야될 것
데이터가 0이라면 아예 출력 X
-> 전부 문자열로 넣어서 마지막에 출력하기
"""

def get_PaddingSize(st_Data, end_Data): # 비트연산을 위한 패딩함수
    if (len(st_Data) > len(end_Data)):
        return len(st_Data)
    elif (len(st_Data) < len(end_Data)):
        return len(end_Data)
    else:
        return len(st_Data)

def get_LBA(type):
    offset = 8
    data_raw = binascii.hexlify(f.read(offset)) # 파일을 읽으면 자동으로 offset이 마지막으로 읽은 위치로 이동됨
    data_raw = hex2bin(data_raw)

    data_Raw_List_St = data_raw.split(' ')[:8] # 8 byte
    data_Raw_List_St.reverse() # Little endian -> Big endian
    raw_Data_st = ''.join(data_Raw_List_St).lstrip('0') # delete '0'

    return raw_Data_st

def hex2bin(rawData):
    cnt = 0
    data = ''
    for i in rawData:  # 바이너리로 변환
        cnt += 1
        data += chr(i)
        if (cnt % 2 == 0):
            data += ' '
            cnt = 0

    return data

def isDataNull(stData, endData):
    if(stData or endData):
        if(endData - stData <= 0):
            return True
        else:
            return False

def get_Partition(f, sector):
    data_raw = []
    f.seek(sector, 0) # 파일 포인터를 entry의 시작주소로 초기화

    # GET Partition_Type_GUID (File System Type)
    for i in range(0, 2):
        offset = 16
        # print Entry
        data_raw.append(binascii.hexlify(f.read(offset))) # offset move 16 byte
        # [0] = File System Type, [1] = GUID
    #print(f"{hex2bin(data_raw[0]).upper()}", end="") # 바이너리를 헥스로 변환
    #print(f"File System Type: {hex2bin(data_raw[1]).upper()}")

    # get GUID
    #f.seek(offset, 1)  # 다음 출력 전으로 이동 # offset move 16 byte

    # st_LBA = 8 byte #
    #print(f.tell())
    raw_Data_St = get_LBA("st_LBA")
    # end_LBA = 8 byte #
    raw_Data_End = get_LBA("end_LBA")

    """
    ending LBA: raw_Data_End
    starting LBA: raw_Data_St
    """

    #print(int(raw_Data_St, 16), end="")

    if(raw_Data_St and raw_Data_End): # 둘 다 값이 있을때만 출력
        print(f"{hex2bin(data_raw[0]).upper()} {int(raw_Data_St, 16)} {int(raw_Data_End, 16) - int(raw_Data_St, 16)}")

def get_Header(f, sector):
    # file move seek(1 bytes)
    f.seek(sector) # 파티션 처음 offset 위치

    # read rawdata for (n)
    #print(f"sector: 0 -> signature {f.read(SIGNATURE)}")

if __name__ == '__main__':
    f = open(FILENAME, "rb")
    rawdata = f.read()
    sector = 0

    # get header
    sector += SECTOR_SIZE # move file offset
    get_Header(f, sector) # find file system 88

    sector += 512 # start sector number : 2
    for i in range(0, ENTRY_SIZE):
        # find partition
        get_Partition(f, sector + (i * 128)) # entry size = 128