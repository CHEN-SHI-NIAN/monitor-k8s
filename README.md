# 題目
## https://hackmd.io/@JeremyCREAM/HkkYv3ICd
# 專案介紹：市場監控系統
## 
這個專案旨在實現一個市場監控系統，專注於監控以太坊上的 crUSDC 合約。該系統將定期查詢區塊鏈，以獲取每100個區塊的供應率（supply rate）和借款率（borrow rate），並監控合約相關的事件，如 Mint、Redeem、Borrow 和 RepayBorrow。這將有助於追蹤流動性和借貸活動，為使用者提供實時的市場數據。
## 因需要呼叫以太坊節點 使用前請先註冊infura帳號並申請url 放心不會需要任何費用
## 預期輸出格式

- 每100個區塊的供應率與借款率:
  ```
  { block number } supply rate: { supply rate }
  { block number } borrow rate: { borrow rate }
  ```

- 監控的事件輸出格式:
  ```
  { block number }: { tx hash }
  { minter } Mint { mintTokens } crUSDC with { mintAmount } USDC { tx hash }

  { block number }: { tx hash }
  { redeemer } Redeem { redeemAmount } USDC, burn { redeemTokens } crUSDC

  { block number }: { tx hash }
  { borrower } Borrow { borrowerAmount } USDC

  { block number }: { tx hash }
  { payer } RepayBorrow { repayAmount } USDC for { borrower }
  ```

## 使用到的技術

1. **以太坊智能合約**:
   - 使用 `ethers.js` 來與以太坊區塊鏈互動，查詢合約的供應率和借款率。

2. **Kubernetes (K8s)**:
   - 將應用程式部署在 **Minikube** 環境中，以便進行容器化管理和擴展。

3. **Docker**:
   - 使用 Docker 將應用程式打包成容器，以便於在不同環境中的部署和管理。

4. **Python**:
   - 使用 Python 來編寫監控邏輯，處理 API 請求以及解析事件日誌。

5. **Web3.js 或 ethers.js**:
   - 與以太坊節點交互，實現對合約的查詢及事件監控。

6. **MongoDB** (可選):
   - 若需要儲存監控數據，可以使用 MongoDB 作為資料庫來存儲供應率、借款率和事件記錄。

## 結論

這個市場監控系統將幫助我們獲取有關 **crUSDC** 合約的實時數據，為使用者提供重要的市場見解。通過使用當前流行的技術堆疊，如 Docker、Kubernetes 和以太坊相關技術，這個專案不僅能展示技術實力，還能為後續的擴展和優化奠定基礎。
