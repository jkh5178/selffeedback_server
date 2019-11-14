##소캣 서버 시작하는 메인 파일
##
import socket
import Threadmain
##쓰레드 관리하는 클래스 생성
tm=Threadmain.Threadmain()
##소캣 생성
s = socket.socket()
##ip 제한 및 연결 포트 설정
s.bind(('0.0.0.0', 8090 ))
##최대 받을수 있는 소캣의 갯수, 알아서 늘어난다
s.listen(0)

while True:
    ##소캣이 연결 될때 까지 대기
    client, addr = s.accept()
    ##연결시 client는 연결정보 addr은 (주소, 포트)를 저장 후
    ##쓰레드를 만든다.
    tm.make_thread(socket=client, addr=addr) 