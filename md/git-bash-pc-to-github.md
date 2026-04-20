# Git Bash：將 PC 端變更同步到 GitHub

本文件說明：**當你已經把 GitHub repository clone 到 PC，並且修改好 `.md` 檔後，如何透過 Git Bash，讓 PC 端與 GitHub 端內容一致。**

---

## ✅ 前提條件

在開始之前，請確認以下事項已完成：

- ✅ 已完成 `git clone`
- ✅ 已在 PC 端修改並儲存好 `.md` 檔案
- ✅ 使用 Git Bash，且目前位置在該 repository 資料夾內

---

## 🚶‍♂️ Git 基本同步流程總覽

```bash
git status
git add .
git status
git commit -m "你的修改說明"
git push
```

以下為每一步的詳細說明。

---

## 1️⃣ 進入 repository 資料夾

如果尚未在 repo 目錄內，請先切換目錄：

```bash
cd 你的repo資料夾名稱
```

範例：
```bash
cd vibe-coding-book
```

---

## 2️⃣ 查看目前 Git 狀態

```bash
git status
```

如果你有修改檔案，會看到類似訊息：

```text
modified:   README.md
```

👉 表示 Git 已偵測到檔案變更，但尚未準備送出。

---

## 3️⃣ 將修改加入暫存區（Stage）

### ✅ 加入全部修改（常用）

```bash
git add .
```

### ✅ 或只加入單一檔案

```bash
git add README.md
```

---

## 4️⃣ 再次確認狀態（建議）

```bash
git status
```

看到以下內容代表成功加入暫存區：

```text
Changes to be committed:
  modified: README.md
```

---

## 5️⃣ 建立 Commit（提交修改紀錄）

```bash
git commit -m "更新 README 說明"
```

### ✅ Commit 訊息撰寫建議

- 簡短明確
- 描述「做了什麼修改」

範例：

```bash
git commit -m "新增 Git 操作流程說明"
git commit -m "修正章節 2 的排版"
```

---

## 6️⃣ Push 到 GitHub（同步完成 🎯）

```bash
git push
```

### 🔐 常見情況說明

- 第一次 push：可能會要求登入 GitHub
- HTTPS：需使用 GitHub 帳號 + Personal Access Token
- SSH：設定完成後通常不需再輸入帳密

### ✅ 成功畫面範例

```text
Enumerating objects...
Writing objects...
To https://github.com/rockoak/vibe-coding-book.git
```

➡️ 此時 GitHub 端內容已與 PC 端一致 ✅

---

## 🔁 之後每次更新的標準流程（記住這組）

```bash
git status
git add .
git commit -m "說明這次改了什麼"
git push
```

---

## 🧠 常見新手問題

### ❓ 忘記 `git add` 就 commit

Git 會提示沒有任何變更可提交，請先執行：

```bash
git add .
```

---

### ❓ Push 時出現 rejected / failed

通常是 GitHub 上已有更新，請先同步：

```bash
git pull
```

若有衝突，請先解決後再：

```bash
git push
```

---

### ❓ 尚未 commit，想放棄所有修改

```bash
git restore .
```

---

✅ **完成！**

你現在已完整掌握：
- PC 修改
- Git Bash 提交
- GitHub 同步

建議將此文件保留在你的專案中，作為 Git 操作速查表。
