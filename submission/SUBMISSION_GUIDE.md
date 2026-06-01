# DSP 投稿清单与提交指南

## 一、投稿前你需要做的

### 1. 编译 PDF
在 paper/ 目录下编译 main.tex：
```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
确保编译无错误、无警告。编译出 main.pdf。

### 2. 检查 PDF
- [ ] 页码连续、无异常空白页
- [ ] 所有图表正常显示
- [ ] 参考文献格式正确（Author-Year）
- [ ] 最后一个表格不独占一页
- [ ] 附录排版正常

---

## 二、提交材料清单

在 Elsevier 投稿系统 (https://www.editorialmanager.com/edsp) 中需要上传：

### 必传文件
| # | 文件 | 来源 | 说明 |
|---|------|------|------|
| 1 | **Main Manuscript** | `paper/main.pdf` | LaTeX 编译输出 |
| 2 | **Figures (8张)** | `submission/fig_*.pdf` | 高分辨率 PDF，逐张上传 |
| 3 | **Cover Letter** | `submission/cover_letter.md` | 转为 Word/PDF 上传 |
| 4 | **Highlights** | `submission/highlights.txt` | 在系统中逐条输入 |

### 系统中填写的信息
| 项目 | 内容 |
|------|------|
| Title | Deep-unfolded LISTA for sparse channel estimation: Error concentration and BER implications |
| Authors | Huanjie Yu (Hunan University of Technology and Business) |
| Email | semhaqx@gmail.com |
| ORCID | 0009-0008-9824-1801 |
| Article Type | Research Article |
| Keywords | sparse channel estimation, deep unfolding, ISTA, LISTA, adaptive filtering, compressed sensing |
| Highlights | 5 条（见 highlights.txt） |

### 系统自动生成/已包含在论文中
- Data Availability Statement ✓（论文中）
- Conflict of Interest ✓（论文中）
- CRediT Author Statement ✓（论文中 \printcredits）
- AI Declaration ✓（论文中）

---

## 三、Elsevier 投稿系统提交步骤

### Step 1: 登录
- 打开 https://www.editorialmanager.com/edsp
- 注册/登录账号

### Step 2: Start New Submission
- 选择 "Submit New Manuscript"
- Article Type: **Research Article**

### Step 3: 填写基本信息
- Title: 复制标题
- Abstract: 从论文中复制 abstract
- Keywords: 逐个输入 6 个关键词
- Authors: 添加 Huanjie Yu，设置为 Corresponding Author

### Step 4: 上传文件
- **Item 1**: Main Manuscript → 上传 `main.pdf`
- **Item 2-N**: 每张 figure 单独上传（选 "Figure" 类型）
  - fig_nmse_vs_snr.pdf
  - fig_nmse_vs_sparsity.pdf
  - fig_nmse_vs_channellen.pdf
  - fig_convergence.pdf
  - fig_error_concentration.pdf
  - fig_threshold_comparison.pdf
  - fig_threshold_schedule.pdf
  - fig_ber_nmse_disconnect.pdf
- Cover Letter → 上传 cover_letter（转 PDF）

### Step 5: 输入 Highlights
逐条输入 5 条 highlights（每条一句话）

### Step 6: 建议审稿人（可选）
建议 2-3 位该领域审稿人（非必须但有帮助）

### Step 7: 确认并提交
检查所有信息 → Submit

---

## 四、注意事项

1. **Supplementary Material**：已作为附录包含在 main.tex 中，不需要单独上传
2. **LaTeX 源码**：系统可能会要求上传 .tex + .bib 源码压缩包，把 paper/ 目录打包即可
3. **Figure 格式**：PDF 是首选（矢量图），也可用 TIFF/PNG（≥300 DPI）
4. **Cover Letter**：建议转为 PDF 再上传
5. **审稿周期**：DSP 初审通常 1-2 个月
