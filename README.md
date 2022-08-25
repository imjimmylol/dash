# <center>程式專案說明</center>

## A. 製作算法互動式儀表板
操作步驟：
<br> 
1. 開啟儀表板
```
python index_v2.py
```
2. 找尋區間並輸入

3. 新增資料（使用yfinanceAPI）
```
python updatedata.py -s [start date] -t [ticker]
```
4. 結果呈現
<img src="img\demo.png" width="50%" />

## B. Utils資料夾說明

- algo 
    - calculation # 距離公式都在這裡定義
- data_process
    - input_process # 將輸入標準化，內建4種標準化方法
    - res_process # 刪除輸出重複出現之區間
- plot # 繪圖函式，於dashboard上呈現
- search
    - do_search # 將距離公式apply全部的資料
    - return_res # 直接輸入目標區間，回傳搜尋結果


## C. 後續更新方向

- 在return result中新增開高低收，並進行平均後在寫入字典（現在僅使用收盤價進行搜尋）

- 更改多項式的向量距離表示法
- 多項式分段積分，面積比大小
- 使用者介面優化