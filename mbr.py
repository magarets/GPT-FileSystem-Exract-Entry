import binascii

FILENAME = '../mbr_128.dd'
SECTOR_SIZE = 512
PARTITION_ENTRY_SIZE = 16

EntryList = []
PartitionList = []

def PrintEntryData():
    print(PartitionList[0], EntryList[0], int(EntryList[1], 16) // 512)
    print(PartitionList[1], EntryList[2], int(EntryList[3], 16) // 512)
    print(PartitionList[2], EntryList[4], int(EntryList[5], 16) // 512)

def ReadFileEntry():
    rawData = f.read(PARTITION_ENTRY_SIZE)  # read file for 16byte
    strData = bin2str(rawData)# bin to str

    return strData

def ExractStartAndSize(Data):
    f.seek(-8, 1) # 현재위치에서 8바이트 이전으로 이동
    stEntry = f.read(4)
    sizeEntry = f.read(4)

    # Little endian -> Big endian
    stEntry = bin2str(stEntry)
    sizeEntry = bin2str(sizeEntry)

    StrMakeList(stEntry)
    StrMakeList(sizeEntry)
#    print(f"stEntry(LE): {stEntry}")
#    print(f"sizeEntry(LE): {sizeEntry}")
def bin2str(binData):
    binData = binascii.hexlify(binData)
    strData = binData.decode('ascii')

    return strData

PartitionType = {'00': 'EMPTY', '01': 'FAT12', '04': 'FAT16', '05':'MS Extended', '06':'FAT16', '07':'NTFS', '0B':'FAT32', '0C':'FAT32'}
def GetFileSystemType(Data):
    f.seek(-12, 1) # 16바이트를 읽어서 offset이 16바이트 이후로 이동되어서 offset 뒤로 이동
    bindata = f.read(1) #해당 1바이트만 읽어오기
    f.seek(11, 1) # 읽고나서 offset 원위치

    fileType = bin2str(bindata)

    for key, value in PartitionType.items():
        if fileType == key:
            return value

    return 'Error'

# 문자열을 2개씩 reverse -> little endian -> big endian
def StrMakeList(strData):
    strList = []
    strData = list(strData)
    for i in range(0, len(strData), 2):
        strList.append(''.join(strData[i:i+2]))
    # Little Endian -> Big Endian
    strList.reverse()
    # List -> String
    strData_BE = ''.join(strList)

    strData_BE = strData_BE.lstrip('0')
    EntryList.append(hex(int(strData_BE, 16) * 512))
    # strData_BE : hex data

    return strData_BE

if __name__ == '__main__':
    f = open(FILENAME, 'rb')
    f.seek(446, 0) # 0번째 섹터에서 논리적 파일의 저장위치 값으로 이동

    for i in range(4):
        """
        ReadFileEntry()
        1 ~ 3 : 논리적 저장공간에 저장된 파일 Entry
        4 : 가상 저장공간에 저장된 파일 Entry
        """

        FileEntry = ReadFileEntry()
        ExractStartAndSize(FileEntry)

    f.seek(0)  # 파일 새로 읽기
    f.seek(446, 0)
    for i in range(3):
        FileType = ReadFileEntry()
        PartitionList.append(GetFileSystemType(FileType))

    PrintEntryData()
