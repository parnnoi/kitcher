# kitcher

## How to use

### 1) สร้าง database ชื่อว่า 'kitcher' และใช้ DDL ตามที่แนบไว้ในไฟล์ชื่อ 'DDL.txt'

### 2) สร้างโฟลเดอร์ ชื่อ 'kitcher' ที่ตำแหน่งของ xampp

### 3) กรุณา pull ก่อน push

## Constraints

### 1) ในการ push ให้ push ลงไปที่ branch ของตนเองให้ตั้งชื่อด้วยรูปแบบดังต่อไปนี้
-- 'ชื่อเล่น + xx' (ex. --> 'parn01' โดยให้ xx แทน ตัวเลข 00 - 99 โดยจะเพิ่มตามลำดับของตนเอง)
-- ห้าม push ลง branch 'main' <b>เป็นอันขาด</b>

### 2) การ commit ให้ใส่ 'branchname ที่จะpush' และ 'เหตุผลที่มีการแก้ไข'
-- (ex. 'parn01 เหตุผล แก้ไขจุดผิดพลาดที่ฟังก์ชัน...')

### 3) ในการเขียน code ให้ทุกคนใช้ code standard ตามที่ตกลงกันไว้ งานของตนนั้นอาจถูก reject ได้หากไม่ทำตามข้อกำหนด
-- โดยจะแจ้งว่าให้ไปแก้ด้วยสาเหตุเขียนโค้ดไม่ถูกต้อง แต่จะไม่แจ้งว่าไม่ถูกตรงที่ไหน


## วิธีการ push และ pull กับ branch ของตัวเอง

### 1) ทำการ setup โปรเจคด้วยวิธีการดังต่อไปนี้
-- git init
-- git config user.name "dummyName"
-- git config user.email "gummyEmail@dummy" (กรุณาใช้อีเมลเดียวกับ github)
-- git remote add origin myRepositoryLink
ปล. หากทำงานเก่ามาก่อนจะไม่สามารถ add ได้เพราะเคยสร้าง remote ชื่อ origin ไปแล้ว ต้องไปลบก่อน
-- ลบด้วย git remote rm origin
-- แล้วทำการ git remote add ... ใหม่


### 2) สร้าง branch ของตัวเอง ด้วย "git checkout -b dummyBranchName"

### 3) ใช้ตามปกติ โดยครั้งแรกอาจจะ pull จาก main มาก่อน แล้วพอจะส่งงานกลับขึ้น github ก่อนใช้ push หรือ pull จาก branch ของตัวเอง

# ห้าม push ขึ้น main เด็ดขาด
