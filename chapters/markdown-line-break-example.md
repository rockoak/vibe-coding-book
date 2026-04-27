# Markdown 行尾空格與換行範例

> 本檔案示範 Markdown (.md) 中，不同行尾空格數量造成的顯示差異。
> 適用於 GitLab / GitHub / CommonMark。

---

## 範例一：行尾沒有空格

```md
第一行
第二行
```

顯示結果：

第一行 第二行

---

## 範例二：行尾只有 1 個空格

```md
第一行␠
第二行
```

顯示結果：

第一行 第二行

---

## 範例三：行尾有 2 個空格（重點）

```md
第一行␠␠
第二行
```

顯示結果：

第一行  
第二行

---

## 範例四：行尾有 3 個以上空格

```md
第一行␠␠␠␠
第二行
```

顯示結果：

第一行  
第二行

---

## 結論

- 0 或 1 個空格：沒有任何效果
- **2 個（含）以上空格：等同 HTML `<br>` 強制換行**

---

## 參考文件

- CommonMark 規範：https://spec.commonmark.org/0.30/#hard-line-breaks
- GitHub Flavored Markdown：https://github.github.com/gfm/#hard-line-breaks
