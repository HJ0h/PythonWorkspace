# 은행 프로그램
import os

#계좌정보 관리 클래스
class Account:
    def __init__(self, userid= "", name = "", balance=0):
        if(userid == ""):
            self.userid = int(input("계좌번호 = "))
            self.name = input("고객이름 = ")
            self.balance = int(input("예금금액 = "))
        else:
            self.userid = userid
            self.name = name
            self.balance = balance
            
    # 출력함수
    def disp(self):            
        print("계좌번호: {0}\n이름: {1}\n잔액: {2}".format(self.userid, self.name, self.balance))
    
    # 계좌정보 호출
    def info(self):
        return "계좌번호: {0}\n이름: {1}\n잔액: {2}\n\n".format(self.userid, self.name, self.balance)
    
    # 계좌번호 호출
    def get_id(self):
        return self.userid
    
    # 입금
    def deposit(self, money):
        self.balance += money
        return self.balance
    
    # 출금
    def withdraw(self, money):
        if self.balance < money:
            return 0
        else:
            self.balance -= money
            return money
    
    # 잔액 조회
    def get_Bal(self):     
        return self.balance


# 저장된 계좌 파일 로드
# 리스트 형태로 all_id에 Account객체 append 즉 all_id = Account클래스 객체 리스트
file = "BankBook.txt"
all_id = list()

try:
    with open(file, 'r', encoding='utf-8') as f:
        fcn = 0 # 파일에 기록된 고객 수
        lines = f.readlines()
        ix = 0
        for line in lines:
            ix += 1
            if ix % 5 == 2: # 한 고객 당 5줄 중 2~4줄(계좌번호/이름/잔액)
                second = line.split(":")
            elif ix % 5 == 3:
                third = line.split(":")
            elif ix % 5 == 4:
                fourth = line.split(":")
            elif ix % 5 == 0: # 한 고객 마다 all_id에 Account클래스 객체(계좌) 추가
                all_id.append(Account(int(second[1].rstrip()),third[1].lstrip().rstrip(),int(fourth[1].rstrip())))
                fcn += 1    
except Exception as ex:
    print("파일 없습니다")
    print(ex)

# 화면 초기화                 
def clr():
    os.system('cls')
    

# 계좌정보를 이용하여 구현될 기능을 담고 있는 클래스 멤버필드 
# 멤버메서드 : makeAccount() - 계좌개설을 담당할 메서드
class BankManager:
    # 계좌번호 중복여부 판단
    def new_id(self,user): # Account 객체를 파리미터로 받음             
        for i in all_id:
            if i.get_id() == user.get_id():
                # 불러온 계좌 파일에 저장된 Account객체 계좌번호와 새로 만든 Account객체 계좌번호 비교
                return "입력하신 계좌번호는 이미 존재하는 계좌번호 입니다."
            
        all_id.append(user)
        return "계좌 개설이 완료되었습니다." 
        
    # 입금
    def deposit(self,userid):     
        for i in all_id:
            if i.get_id() == userid:
                money = int(input("입금금액 = "))
                bal = i.deposit(money)
                print("잔액은 {0} 입니다.".format(bal))
                return 0
        print("일치하는 계좌번호가 존재하지 않습니다")


    # 출금
    def withdraw(self,userid):    
        for i in all_id:
            if i.get_id() == userid:
                money = int(input("출금금액 = "))
                return i.withdraw(money)
        print("해당하는 계좌가 없습니다.")

    
    # 계좌정보 전체출력
    def showAccount(self):             
        if len(all_id) != 0:
            for i in range(0,len(all_id)):
                print(f"[{i+1}]")
                all_id[i].disp()
        else:
            print("보유한 계좌가 없습니다.")
                 
    # 파일에 저장
    def save(self, change):
        global fcn
        if change == 0: # 입출금X
            with open(file, 'r', encoding='utf-8') as f: # append
                if fcn == 0: # 파일 내용 empty
                    for i in all_id:
                        f.write(f"[ {fcn+1} 번째 고객 ]\n")
                        f.write(i.info())
                        fcn += 1  
                else: # 내용 有 
                    for i in all_id[fcn:]:
                        f.write(f"[ {fcn+1} 번째 고객 ]\n")
                        f.write(i.info())
                        fcn += 1
        else: # 입출금 > 잔액 변동 : write로 덮어쓰기
            with open(file, 'w', encoding='utf-8') as f:
                cn = 1 # 고객번호
                for i in all_id:
                        f.write(f"[ {j} 번째 고객 ]\n")
                        f.write(i.info())
                        cn += 1   
            

# 은행 시스템 제공 인터페이스 클래스
class BankSystem: 
    def run():
        change = 0 # 입출금으로인한 잔액 변동 체크
        while True:
            print("~ Welcome to our Bank! ~")
            print("[1] 계좌개설")
            print("[2] 입금처리")
            print("[3] 출금처리")
            print("[4] 전체조회")
            print("[5] 프로그램 종료")
            print("#####################")
            menu = input("메뉴를 선택해주세요: ")
            if menu == "1":       # 계좌개설
                clr()
                print("#######계좌개설#######")
                print(BankManager().new_id(Account()))
                print("#####################")
                
            elif menu == "2":     # 입금
                clr()
                print("#######입 금#######")
                userid = int(input("계좌번호 = "))
                BankManager().deposit(userid)
                change += 1
                print("#####################")
                 
                
            elif menu == "3":    # 출금
                clr()
                print("#######출 금#######")
                userid = int(input("계좌번호 = "))
                w = BankManager().withdraw(userid)
                if w != None:
                    print("{0}원 출금하셨습니다.".format(w))
                    change += 1
                
            elif menu == "4":
                clr()
                print("#######조 회#######")
                BankManager().showAccount()
                print("#####################")
                
            elif menu == "5":
                BankManager().save(change)
                print("종료합니다.")
                break


if __name__ =='__main__':
    BankSystem.run()
