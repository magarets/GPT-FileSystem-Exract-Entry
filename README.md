# GPT-FileSystem-Exract-Entry

* Sector SIZE: 512 byte<br>
* Storage infomation for each sector<br>
#1: MBR <br>
#2: GPT Header<br>
#3 ~ 34: GPT File info <br><br>
GPT 파일 시스템에서는 하나의 섹터마다 4개의 Entry가 존재합니다.<br>
각각의 Entry는 하나의 파일에 대한 정보를 저장하고 있습니다.<br>
<img width="621" alt="image" src="https://user-images.githubusercontent.com/101767824/185342142-777b76b0-7d79-478a-b643-7bc3cf605944.png">
<br>
Starting LBA for partitions : 파티션의 논리적 시작 주소<br>
Ending LBA for partitions : 파티션의 논리적 끝 주소<br>
Number of partition entries : 파티션 엔트리의 개수 (0x80의 값을 지님)<br>
Size of each entry : GPT entry의 크기 (0x80의 값을 지님)<br>
