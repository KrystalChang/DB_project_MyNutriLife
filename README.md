# 113-1 資料庫管理 - MyNutriLife 專案

## 專案簡介

「MyNutriLife」是一款個人健康營養管理系統，旨在幫助使用者記錄日常飲食，並根據國民健康署公布的「國人膳食營養素參考攝取量」第八版（DRI）提供個人化的營養建議。系統以真實的「食品營養成分資料集」（來自政府資料開放平臺）為基礎，允許使用者記錄每日食物攝取量，系統則自動計算營養素攝取情況，並與建議值對比，提供達成率分析。此外，系統設計還包含了文章瀏覽和收藏清單等功能，以供使用者的閱讀相關營養保健知識。
此系統的設計涵蓋兩類主要使用者：「一般使用者」（User）和「業務經營者」（Operator）。User 是系統的主要使用對象，任何社會大眾都可以是一般使用者，可以記錄和查詢個人飲食紀錄，並進行營養成分攝取的對比查詢；Operator 則是具有醫療或營養相關背景的專家，例如：醫師、藥師、營養師等，可撰寫與發佈營養保健文章，以便 User 可獲得他們有興趣的飲食建議。

:link: **[展示影片連結](https://youtu.be/pK8TacgzC4E)**

## 使用者功能

### User （一般使用者）

#### 使用者登入、註冊

- 註冊：使用者可以註冊帳號設定使用者名稱、密碼及電子郵件信箱，以及基本資訊（包含生日、性別），系統會分配一個 user_id 給每位使用者。
- 登入：透過使用者名稱及密碼登入。

#### 瀏覽文章並收藏至最愛

- 瀏覽文章：使用者可以瀏覽業務經營者已發布的文章，系統會先呈現文章標題供使用者選擇，再呈現對應標題的文章內容。
- 收藏至最愛：文章瀏覽完畢後，系統會詢問使用者是否要將該文章收藏至最愛。使用者可以將有興趣或認為重要的文章添加至最愛清單，以便於日後查找及複習。

#### 瀏覽或移除最愛的文章

- 系統會先呈現最愛的文章標題供使用者選擇，接著使用者可以選擇要瀏覽或移除已設置為最愛的文章。
- 瀏覽最愛：呈現使用者所選擇之標題對應文章內容。
- 移除最愛：將使用者所選擇的標題之文章從最愛中移除。

#### 每日飲食紀錄

- 使用者可以記錄每日飲食，包括進食日期和時間，以及所吃的食品名稱和攝取量。

#### 查看（刪除）飲食紀錄

- 查看：系統會請使用者輸入開始日期與結束日期。使用者可以查看歷來飲食紀錄，了解特定日期所吃的食品名稱與攝取量。
- 刪除：系統會詢問使用者是否要刪除任何內容，若有需要則會請使用者輸入該筆紀錄相關資料以刪除紀錄。

#### 營養攝取情況分析

- 情況分析：使用者可以查看歷來的營養攝取情況。系統會請使用者輸入開始日期與結束日期，以及想了解攝取情況的營養素名稱（目前僅供搜尋「熱量、總碳水化合物、膳食纖維」），並呈現期間內各日期的特定營養素當日總攝取量以及 CSR（「當日總攝取量」和「DRI」表中的「建議攝取量」的比值）協助使用者了解自己是否達到當日營養素所需的標準或是否超過建議的上限量，以幫助使用者進行健康管理。
- 繪成圖表：使用者可以選擇是否要生成圖表，呈現 CSR 在該期間內的變化以便觀察和追蹤長期飲食趨勢。

#### 查詢食品營養成分

- 查詢：使用者可以輸入食品的關鍵字，查詢特定食品的詳細營養成分。系統會顯示所選食品的各種營養素含量，包括熱量、蛋白質、脂肪、維生素等。此功能讓使用者對所選食物有更深入的了解，幫助他們做出更合理的飲食選擇。

### Operator （管理員／業務經營者）

在本系統中，Operator（業務經營者）可以執行以下功能：

#### 註冊與登入

- 註冊：管理員可以註冊帳號設定使用者名稱、密碼及電子郵件信箱，系統會分配一個 o_id 給每位管理員。
- 登入：透過信箱及密碼登入。

#### 撰寫文章

- 業務經營者可以撰寫並發布文章，包括選擇標題和撰寫內容，以提供使用者閱讀。

#### 編輯、刪除文章

- 業務經營者可隨時修改或刪除文章，確保文章內容符合最新的營養研究趨勢與健康指引，為使用者提供具參考價值的健康資訊。

## 使用方法

- 使用備份檔 `DB.backup` 復原資料庫
- 預設連線通道為 **127.0.0.1:8800**，可至 `server.py` 及 `client.py` 修改
- 在 `DB_utils.py` 設定**資料庫名稱** (dbname)、**使用者名稱** (user)、**資料庫密碼** (password)、**主機位置** (host)及**通訊埠** (port)

先執行 `server.py` 啟動伺服器：

```bash
python server.py
```

再開啟另一個終端機執行 `client.py` 向伺服器連線：

（註：記得要先在終端機將檔案導入到正確的路徑）

```bash
python client.py
```

**Notes:** 功能 `[2] List All Available Study Events` 因為 query 的資料量太大，需等待約半分鐘的資料傳遞，以及連線介面的 Scrollback Buffer 建議調大才能看到所有輸出。

## 技術細節

- 使用 Socket 建立 client-server 連線，搭配 Multithreading 達成多人同時連線

- 資料庫使用 PostgreSQL，使用套件 Psycopg2 對資料庫進行操作

- **交易管理 & 併行控制**：可參考 `./DB_util.py` 中的 `db_update_article()`

## 程式說明

1. **`./server.py`**
   - 包含伺服器端的主要功能。
   - 在連接資料庫後，透過 socket 建立監聽服務，接收來自客戶端的連線請求。
   - 每當接收到一個客戶端連線，會啟動一個獨立的執行緒（thread）處理該連線，確保伺服器能並行處理多個客戶端。
2. **`./client.py`**
   - 包含客戶端的主要功能。
   - 持續從伺服器接收訊息並顯示於終端機。
   - 當訊息包含特定標籤（tag）時，根據標籤執行對應的操作，例如讀取使用者輸入、解析 CSV 檔案、關閉 socket 連線並結束程式。
3. **`./DB_utils.py`**
   - 封裝與資料庫相關的功能，包含資料庫連線管理與查詢操作。
4. **`./action` 資料夾**
   - 每項執行動作被實作為一個類別，繼承抽象類別 `Action`，並實作其核心方法 `exec()`。
   - 此架構讓程式具備高度擴展性，開發者可透過新增 action 類別輕鬆增加新功能。

## 開發環境

- Python: 3.10.9
- PostgreSQL: 16.4



## 可供測試的 User 帳號（因為密碼有加密，因此這邊提供可測試的 User 帳密）

- 名稱：dennis86、密碼：6%gPL@Wa#O
  
- （如果想測試其他 User 請見：https://drive.google.com/file/d/1xKCAV6QiQpzaR50unlATCMG41fqLzwRy/view?usp=sharing）

- 可供測試的 Operator 帳號：johnodom@example.com、密碼：L5fRF+Et(A

- （如果想測試其他 Operator 請見：https://drive.google.com/file/d/1zsG3cqIXHQUSzkSpVitU3b-kPkC8UfRO/view?usp=sharing）

## 參考資料

- README 說明文件及報告內容來自 **113-1 資料庫管理 第四組**
