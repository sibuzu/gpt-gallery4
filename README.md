# Gallery 4

遊戲與動漫角色圖庫，目標網址為 https://gallery4.sibuzu.com。

沿用 Gallery 3 的網站結構、分類展開／收合、搜尋、圖片燈箱及同名 `.md` PROMPT 查看／複製功能。只有 `images/` 下已有圖片的角色會出現在圖庫；尚未有圖的 PROMPT 不會產生空白圖片卡。來源 PNG 與 PROMPT 保持原樣。

網頁預設展開所有分類；可手動收合與再次展開，重新整理後恢復全部展開。

圖片網格最多 4 欄；桌面顯示 4 欄，窄螢幕自動切換為 2 欄或 1 欄。

圖片卡片左下以「《作品》角色名」顯示，例如「《快打旋風》Rose」，右側為 PROMPT 等操作按鈕。

從主 repository 根目錄建置：

```bash
.venv/bin/python scripts/build_gallery.py --site gallery4
```

也可執行 `.venv/bin/python sites/gallery4/build_gallery.py`。建置直接更新本目錄的 `scripts/gallery-data.js`、`catalog_report.json` 及 `index.html` 資產版本，不產生 `dist/`，也不更名或修改任何圖片或 PROMPT。

GitHub repository： https://github.com/sibuzu/gpt-gallery4 ，正式分支為 `main`。

Netlify 選擇 **Import an existing project → GitHub → sibuzu/gpt-gallery4**，使用下列設定：

| 設定 | 值 |
| --- | --- |
| Branch to deploy | `main` |
| Base directory | 留空（repository 根目錄） |
| Package directory | 留空 |
| Build command | `python3 build_gallery.py` |
| Publish directory | `.` |
| Functions directory | 留空 |
| Python version | `3.12`（已設定於 `netlify.toml`） |

`netlify.toml` 已包含建置設定；Netlify 會從根目錄的 `requirements.txt` 安裝 Python 依賴。不需使用 Netlify CLI 登入或上傳 `dist/`。

在 **Domain management** 新增 `gallery4.sibuzu.com`，並在 DNS 供應商設定：

| 類型 | 名稱 | 目標 |
| --- | --- | --- |
| CNAME | `gallery4` | Netlify 實際分配的 `<site-name>.netlify.app` |

以 Netlify 顯示的實際 hostname 為準；待網域驗證及 HTTPS 憑證完成後驗證正式網址。GitHub `main` 後續推送由 Netlify 自動建置與發佈。不要在 repository 放入登入憑證。
