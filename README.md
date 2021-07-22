## Othello

- **背景介紹**：ML 寫不出來，codeforce 題解看不懂，於是乎跑去研究 GUI 下的產物。

- **內容**：以 tkinter 實作 Othello 的 GUI。

- **更新**：
  | 更新日期 | 說明 |
  | --- | --- |
  | 2021/07/10 | 完成 Othello 的 GUI 介面 |
  | 2021/07/16 | 修復一方無法移動時，遊戲會直接結束的問題 |
  | 2021/07/16 | 加入 minimax、alpha-beta-pruning 實現 AI agent |
  | 2021/07/22 | 將程式模塊化，優化效率 |
  | 2021/07/22 | 修復下玩棋後看不到落子，等 AI 落子才一起渲染的問題 |
  | 2021/07/22 | 增加靈活度，包含 AI agent 之間的對弈，調整盤面大小等 |

- **執行**：

  - `python3 main.py -b 8`
  - `-b`：此參數為盤面大小，若不設定默認為 8。

- **8 x 8 盤面的 minimax 評估函數**：
  | 方式 | 說明 |
  | --- | --- |
  | 以黑子、白子數量判別盤面 | 在前期會因為多吃幾個子而放棄重要的位置，諸如邊角等 |
  | 以加權方式計算分數 | 按常見的評估方式給不同位置不同的權重分數，諸如角 > 邊 > 腹地，但隨著遊戲進行，角的重要性會下降，agent 依然有可能為了邊角放棄腹地的多個棋子 |
  | 以加權方式計算分數，線性收斂至相同權重 | 為平衡前面兩種評估方式的問題，改用動態權重的方式，隨著遊戲進行，不同位置棋子的價值差距會衰減，直到價值相同 |

- **Demo**：開始時預設為 AI agent 對弈，而後可自己選擇模式

- **可能的更新**：
  - **評估函數**：現在 8 x 8 盤面的評估函數是經過設計的，其餘盤面大小，未設計特定的啟發函數。
  - **AI agent 方法**：考慮使用除 Minimax 外的方式實作。
  - **CMD 模式**：GUI 的渲染會浪費許多時間，若單純測試 AI agent 透過 CMD 介面會更便利。
