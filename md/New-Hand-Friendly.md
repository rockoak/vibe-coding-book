# New-Hand-Friendly.md

# 🌱 新手友善版：用 Git Bash 把 PC 修改同步到 GitHub

本章節適合 **第一次接觸 Git / GitHub 的新手**，內容已特別調整語氣與結構，並可直接放入 **vibe-coding-book** 作為實作指南。

---

## 🎯 這一章你會學到什麼？

- 什麼是「PC 端」與「GitHub 端」同步
- 修改 `.md` 後，**一定要做的 4 個指令**
- 每個指令在做什麼（不背指令也能懂）
- 出錯時，該怎麼排查與補救

---

## 🧠 先用一句話理解 Git

> **Git 就像「存檔系統」**，而 GitHub 是「幫你存檔的雲端空間」。

你現在做的是：

> ✏️ 在自己電腦改檔案 → 📦 打包修改 → ☁️ 上傳到 GitHub

---

## ✅ 開始前，請確認已完成

- ✅ 已用 `git clone` 把專案抓到電腦
- ✅ 已經打開並修改 `.md` 檔，且「有存檔」
- ✅ 用 **Git Bash**，且目前在專案資料夾內

---

## 🚶‍♂️ 新手版「最小可用流程」（一定要記住 ⭐）

> **你只要記住這 4 行，就可以活下來** 😄

```bash
git status
git add .
git commit -m "說明你改了什麼"
git push
```

下面一行一行來解釋。

---

## 1️⃣ git status｜先看看 Git 怎麼看你

```bash
git status
```

你可能會看到：

```text
modified: README.md
```

✅ 意思是：
- 你電腦上的檔案「真的有改到」
- 但 Git 還沒幫你記錄

👉 **習慣每次操作前，先打 `git status`**

---

## 2️⃣ git add .｜告訴 Git：這些修改我要存

```bash
git add .
```

🔍 白話解釋：
- 把「剛剛改的東西」放進準備存檔的盒子
- `.` 代表「全部修改過的檔案」

---

## 3️⃣ git commit｜真的存成一個版本

```bash
git commit -m "新增 Git 新手教學"
```

📌 commit 可以想成：
- 遊戲的「存檔點」
- 每一個 commit 都是一個歷史紀錄

✅ 訊息原則：
- 說「你做了什麼」
- 不用太華麗，但要看得懂

---

## 4️⃣ git push｜上傳到 GitHub（完成 🎉）

```bash
git push
```

🚀 這一步做的事：
- 把你電腦的 commit
- 傳送到 GitHub

成功後，你在 GitHub 網站上就會看到一模一樣的內容。

---

## 🧭 初學者流程圖（記住這張就好）

```text
┌────────────┐
│ 修改 .md   │
└─────┬──────┘
      ▼
┌────────────┐
│ git status │ ← 檢查有沒有改到
└─────┬──────┘
      ▼
┌────────────┐
│  git add . │ ← 放進暫存區
└─────┬──────┘
      ▼
┌────────────┐
│ git commit │ ← 存成一個版本
└─────┬──────┘
      ▼
┌────────────┐
│ git push   │ ← 上傳 GitHub
└────────────┘
```

---

## 🧰 新手最常見錯誤 & 解法

### ❌ 打了 git commit，但說「nothing to commit」

👉 原因：你忘了 `git add`

✅ 解法：
```bash
git add .
```

---

### ❌ git push 失敗（rejected / rejected non-fast-forward）

👉 原因：GitHub 上有較新的版本

✅ 解法（安全版）：
```bash
git pull
git push
```

---

### ❌ 改到亂掉，想全部放棄（還沒 commit）

✅ 解法：
```bash
git restore .
```

---

## 📘 放進 vibe-coding-book 的建議方式

建議結構：

```text
vibe-coding-book/
├─ docs/
│  └─ New-Hand-Friendly.md   ✅（本檔案）
├─ README.md
```

並在 `README.md` 加上一行：

```md
- 📘 Git 新手教學：docs/New-Hand-Friendly.md
```

---

## ✅ 本章小結

你現在已經會：

- 在 PC 修改檔案
- 用 Git Bash 存成 commit
- 推送到 GitHub
- 看懂錯誤並自救

> 🎯 **新手目標不是記住全部指令，而是會照流程走。**

---

👉 下一章可以學：
- 多人協作怎麼用 Git
- 為什麼要開 branch
- GitHub Pull Request 是什麼
