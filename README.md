# Factor-Analysis

# 因子研究框架

## **Backtest : 進出場訊號與報酬計算**
<br>

```python
class Backtest:
    """
    sim(): 模擬回測績效並產生各類報表
    """
```

### **sim**  
<br>

```python
sim(position: pd.DataFrame)
```
> 模擬回測績效並產生各類報表

---

<br>
<br>

## **Report : 回測結果分析**
<br>

```python
class Report:
    """
    display(): 繪製淨值走勢圖
    stats(): 詳細回測數據
    """
```

### **display**  
<br>

```python
display(name: str = 'Unnamed Factor')
```
> 繪製淨值走勢圖

---

### **stats**  
<br>

```python
stats()
```
> 詳細回測數據

---

<br>
<br>

## **因子庫**
<br>

### **CPV**  
<br>

```python
CPV(data: pd.DataFrame)
```

<br>
<br>

## **簡易範例**
<br>

### **價量 CPV 因子**
<br>

---

```python
from factor import *
import pandas as pd
import warnings 
warnings.filterwarnings("ignore")

df = pd.read_feather('5min_kbars.ftr')

factor = CPV(df)
report = factor.sim(ngroups=10)
report.display('CPV')
```

> Step 1: 將 factor.py 與 報酬指數.ftr 放至回測程式檔案之同層資料夾並 import

> Step 2: 利用 pd.read_feather() 或 pd.read_csv() 讀入 OHLCV 及需要使用的資料 

> Step 3: 使用 factor 因子庫中對應的因子函式產生因子值樞紐表

> Step 4: 決定分組數後放入 sim() 函式之參數即可透過 display() 產生因子結果
