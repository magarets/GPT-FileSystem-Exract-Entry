"""
format : bytes
output : {GUID} {FileSystem Type} {실제 리얼 offset sector = byte} {사이즈 = byte}
"""
import binascii
import sys

SECTOR_SIZE = 512
PARTITION_SIZE = 128
SIGNATURE = 8
HEADER_SIZE = 4

FILENAME = "../gpt_128.dd"

def get_PaddingSize(st_Data, end_Data): # 비트연산을 위한 패딩함수
    if (len(st_Data) > len(end_Data)):
        return len(st_Data)
    elif (len(st_Data) < len(end_Data)):
        return len(end_Data)
    else:
        return len(st_Data)

def get_EntrySize(st_Data, end_Data): #논리주소가 가르키는 Entry의 Size 계산
    ## padding bytes ##
    """
    paddingSIZE = get_PaddingSize(st_Data, end_Data)

    st_Data = '0' * (paddingSIZE - len(st_Data)) + st_Data
    end_Data = '0' * (paddingSIZE - len(end_Data)) + end_Data
    """
    if(st_Data or st_Data): # 값이 없을 때 까지 출력
        if(int(end_Data, 16) - int(st_Data, 16) == 0):
            return 0
        else:
            return int(end_Data, 16) - int(st_Data, 16)

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

def get_Partition(f, sector):
    data_raw = []
    f.seek(sector, 0) # 파일 포인터를 entry의 시작주소로 초기화
    print(f"start offset : {f.tell()}") # 현재 entry의 상대적인 시작 위치 출력

    # GET Partition_Type_GUID (File System Type)
    for i in range(0, 2):
        offset = 16
        # print Entry
        data_raw.append(binascii.hexlify(f.read(offset))) # offset move 16 byte
        # [0] = File System Type, [1] = GUID
    print(f"GUID: {hex2bin(data_raw[1])}") # 바이너리를 헥스로 변환
    print(f"File System Type: {hex2bin(data_raw[0])}")

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

    EntrySize = get_EntrySize(raw_Data_St, raw_Data_End)
    if(not EntrySize):
        sys.exit()
    print(f"Entry Size : {EntrySize}")


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
    sector += 512 # move file offset
    get_Header(f, sector) # find file system

    sector += 512 # start sector number : 2
    for i in range(0, 128):
        # find partition
        get_Partition(f, sector + (i * 128)) # entry size = 128
        print("-" * 40)
