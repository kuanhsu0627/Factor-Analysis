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
