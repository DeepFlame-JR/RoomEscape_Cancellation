# Find_Cancellation
방탈출 Decoder의 Tempo Rubato 테마 취소 자리 찾기 프로젝트입니다.   
   
## Purpose
방탈출 테마 중 Decoder는 1년간 예약이 꽉 차있습니다.   
1년 뒤 열리는 자리를 예약하는 것보다 취소 자리를 찾는 것이 좀 더 합리적일 것이라 생각했습니다.   
따라서 예약이 취소되는 자리를 주기적으로 확인하여 이메일을 전송하도록 구현했습니다.   
   
## Service
※ 2022년 6월부로 해당 프로젝트는 종료되었습니다.😥  
   
~~아래 주소에서 이메일을 등록하시면 빈 자리 알림을 받으실 수 있습니다! 😀   
http://52.79.88.245:3001/~~  
   
<img width="60%" src="https://user-images.githubusercontent.com/40620421/157457764-4f39e37f-9ee8-48b2-8167-634c628c3ebf.png"/>   
   

   
---

## Solution
1. selenium을 통해서 웹 컨트롤과 크롤링을 진행하여 예약 취소되는 자리가 있는지 확인한다.
2. 취소되는 자리를 확인하면 메일을 보내 이를 알린다.   
   2-1. 특정 user에게 특정 취소 자리 시간을 최초로 전송하는 경우   
   2-2. 특정 user에게 특정 취소 자리 시간을 전송한 기간이 하루가 지났을 경우   
3. 위 과정을 AWS EC2를 활용하여 진행한다. 이를 통해 24시간 주기적으로 확인함을 보장한다.
   
## Environment
AWS EC2   
Ubuntu:20.04   
- Python (selenium, smtplib)
- MongoDB
- node.js, npm
