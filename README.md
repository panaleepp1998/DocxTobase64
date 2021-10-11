# cloud-run-product-search 

เป็นการทำงาน API ที่ใช้ เครื่องมือ
  - python fastapi
  - python opencv
  - docker
  - deploy google clond run
 
#ขั้นตอนการสร้าง image บน docker 

    % docker-compose up -d
    
#คำสั่งพื้นฐาน Docker
  
  แสดง images ทั้งหมด 
  
    % docker images
    
  แสดง images ที่ run อยู่
    
    % docker ps
    
  ลบ images
    
    % docker image rm {ชื่อ image}
  
  
#ขั้นตอนการสร้าง image บน google registry
  1. login "gcloud init" บน folder project
  2. เลือก project บน เแย
  3. ใช้คำสั่ง
  
    % docker pull {ชื่อ image}
    % docker tag {ชื่อ image} asia.gcr.io/{ชื่อ project-gcp}/{ชื่อ image}
    % docker push asia.gcr.io/{ชื่อ project-gcp}/{ชื่อ image}
    
จากนั้นก็ สร้าง service บน cloud run โดยกำหนด port เป็น 80
