# Find_Cancellation
방탈출 테마 Decoder 자리 찾기 프로젝트입니다.   
   
자세한 내용: https://deep-flame.tistory.com/6

## Purpose
방탈출 테마 중 Decoder는 1년간 예약이 꽉 차있다.   
따라서 예약 취소되는 자리를 주기적으로 확인하여 메시지가 오도록 구현할 것이다.   
    
      
---

## Solution
1. selenium을 통해서 웹 컨트롤과 크롤링을 진행하여 예약 취소되는 자리가 있는지 확인한다.
2. 취소되는 자리를 확인하면 메일을 보내 이를 알린다.
3. 위 과정을 AWS EC2를 활용하여 진행한다. 이를 통해 24시간 주기적으로 확인함을 보장한다.
   
## Flow
<img width="60%" src="https://user-images.githubusercontent.com/40620421/154963593-f7ac8c09-a401-4623-bb6a-71cedff58042.png"/>

   
## Installation
코드를 실행하기 위한 설치사항
- Python
- selenium
- smtplib
