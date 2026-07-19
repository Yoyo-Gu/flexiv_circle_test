# 四个 Python 文件逐行解释

这份说明对应当前目录下的四个文件：

```text
config.py
trajectory.py
plot_trajectory.py
main.py
```

当前这四个文件只用于本地生成和检查圆形轨迹，不会连接非夕机械臂，也不会发送真实运动命令。

## 1. config.py

这个文件负责保存默认参数。把参数单独放在这里，以后想改圆心、半径、点数时，不需要去主程序里到处找。

### 第 1 行

```python
"""Default parameters for local trajectory generation."""
```

这是文件说明，也叫模块 docstring。

意思是：这个文件保存本地轨迹生成用的默认参数。

它不会影响程序逻辑，只是帮助人理解这个文件的用途。

### 第 2 行

```python

```

这是空行。

作用是把文件说明和后面的参数隔开，让代码更清楚。

### 第 3 行

```python
CIRCLE_CENTER = (0.3, 0.0, 0.4)
```

定义圆心位置。

`CIRCLE_CENTER` 是变量名，表示 circle center，也就是圆形轨迹的中心点。

`(0.3, 0.0, 0.4)` 是一个三元组，分别表示：

```text
x = 0.3 m
y = 0.0 m
z = 0.4 m
```

单位是米。

这只是本地画图和学习用的默认值，不代表真实机械臂一定安全。

### 第 4 行

```python
CIRCLE_RADIUS = 0.03
```

定义圆的半径。

`0.03` 的单位是米，也就是 3 cm。

这个值比较小，适合先做学习和低风险的轨迹验证。

### 第 5 行

```python
CIRCLE_POINTS = 120
```

定义圆形轨迹由多少个点组成。

这里是 120 个点。

点越多，画出来的圆越平滑；点太少，圆会更像多边形。

### 第 6 行

```python

```

这是空行。

作用是把圆形参数和输出文件名分开。

### 第 7 行

```python
DEFAULT_OUTPUT = "circle_trajectory.png"
```

定义默认保存图片的文件名。

当你运行：

```bash
python main.py --shape circle
```

如果没有自己指定 `--output`，程序就会把图保存成：

```text
circle_trajectory.png
```

## 2. trajectory.py

这个文件负责生成轨迹点。

它只做数学计算，不导入非夕 RDK，也不控制机械臂。

### 第 1 行

```python
"""Pure trajectory generation functions.
```

这是文件说明的第一行。

意思是：这个文件里放的是纯轨迹生成函数。

### 第 2 行

```python

```

这是文件说明中的空行，用来分隔标题和详细说明。

### 第 3 行

```python
This module does not import or call Flexiv RDK. It only generates points that
```

这是文件说明的一部分。

意思是：这个模块不会导入或调用 Flexiv RDK。

也就是说，这个文件不会连接机器人。

### 第 4 行

```python
can be plotted locally and later converted into robot commands.
```

这是文件说明的继续。

意思是：这里生成的点可以先在本地画图，以后再转换成机器人运动命令。

### 第 5 行

```python
"""
```

这是文件说明的结束。

三引号 `"""` 成对出现，第 1 行开始，第 5 行结束。

### 第 6 行

```python

```

这是空行，用来分隔文件说明和导入语句。

### 第 7 行

```python
from __future__ import annotations
```

这行是 Python 的未来特性导入。

它让类型标注的处理更灵活。

在这个项目里，它主要是为了让类型提示更现代、更稳定。

你现在可以先简单理解为：它不改变轨迹数学，只是帮助 Python 更好地处理类型标注。

### 第 8 行

```python

```

这是空行，用来分隔不同类型的导入。

### 第 9 行

```python
import numpy as np
```

导入 `numpy`，并把它简写成 `np`。

`numpy` 是用来做数值计算的库。

后面会用到：

```text
np.linspace
np.pi
np.cos
np.sin
np.full_like
np.column_stack
```

### 第 10 行

```python

```

这是空行，用来分隔导入语句和函数定义。

### 第 11 行

```python

```

这是第二个空行。

Python 代码风格里，通常用两个空行分隔顶层函数。

### 第 12 行

```python
def generate_circle(
```

开始定义一个函数。

函数名是 `generate_circle`。

它的作用是生成圆形轨迹点。

这一行只有函数定义的开头，因为参数比较多，所以分成多行写。

### 第 13 行

```python
    center: tuple[float, float, float],
```

定义函数的第一个参数 `center`。

`center` 表示圆心。

`tuple[float, float, float]` 是类型提示，意思是它应该是 3 个浮点数组成的元组。

例如：

```python
(0.3, 0.0, 0.4)
```

### 第 14 行

```python
    radius: float,
```

定义函数的第二个参数 `radius`。

`radius` 表示圆半径。

`float` 表示它应该是浮点数，例如 `0.03`。

### 第 15 行

```python
    num_points: int,
```

定义函数的第三个参数 `num_points`。

它表示要生成多少个轨迹点。

`int` 表示它应该是整数，例如 `120`。

### 第 16 行

```python
) -> np.ndarray:
```

结束函数参数列表。

`-> np.ndarray` 是返回值类型提示。

意思是：这个函数会返回一个 numpy 数组。

冒号 `:` 表示函数体从下一行开始。

### 第 17 行

```python
    """Generate a closed circle trajectory in the x-y plane.
```

这是函数说明的第一行。

意思是：生成一个在 x-y 平面上的闭合圆形轨迹。

“闭合”表示最后一个点会回到起点。

### 第 18 行

```python

```

这是函数说明里的空行。

### 第 19 行

```python
    Args:
```

函数说明里的参数说明部分。

`Args` 表示下面开始解释这个函数接收哪些参数。

### 第 20 行

```python
        center: Circle center as ``(x, y, z)`` in meters.
```

解释 `center` 参数。

意思是：`center` 是圆心，格式是 `(x, y, z)`，单位是米。

### 第 21 行

```python
        radius: Circle radius in meters.
```

解释 `radius` 参数。

意思是：`radius` 是圆半径，单位是米。

### 第 22 行

```python
        num_points: Number of points along the circle, including the final
```

解释 `num_points` 参数的第一部分。

意思是：`num_points` 表示沿圆形轨迹生成的点数。

这一行还没说完，下一行继续。

### 第 23 行

```python
            repeated point that closes the trajectory.
```

继续解释 `num_points`。

意思是：这些点里包括最后那个用来闭合轨迹的重复点。

例如起点是圆右侧，最后一个点也回到圆右侧。

### 第 24 行

```python

```

这是函数说明里的空行。

### 第 25 行

```python
    Returns:
```

函数说明里的返回值说明部分。

`Returns` 表示下面解释这个函数会返回什么。

### 第 26 行

```python
        A ``(num_points, 3)`` array. Each row is ``[x, y, z]``.
```

解释返回值。

意思是：返回一个形状为 `(num_points, 3)` 的数组。

每一行都是一个轨迹点：

```text
[x, y, z]
```

### 第 27 行

```python
    """
```

函数说明结束。

### 第 28 行

```python
    if radius <= 0:
```

检查半径是否合法。

如果半径小于或等于 0，就不合理。

圆的半径必须是正数。

### 第 29 行

```python
        raise ValueError("radius must be greater than 0")
```

如果半径不合法，就主动报错。

错误信息是：

```text
radius must be greater than 0
```

这样可以避免后面生成错误轨迹。

### 第 30 行

```python
    if num_points < 4:
```

检查点数是否合法。

如果点数少于 4，就太少了，无法合理表示一个圆。

### 第 31 行

```python
        raise ValueError("num_points must be at least 4")
```

如果点数太少，就主动报错。

错误信息是：

```text
num_points must be at least 4
```

### 第 32 行

```python

```

这是空行。

作用是把参数检查和真正的轨迹计算分开。

### 第 33 行

```python
    center_x, center_y, center_z = center
```

把圆心拆成三个变量。

如果：

```python
center = (0.3, 0.0, 0.4)
```

那么这行之后：

```text
center_x = 0.3
center_y = 0.0
center_z = 0.4
```

### 第 34 行

```python
    theta = np.linspace(0.0, 2.0 * np.pi, num_points)
```

生成一串角度值。

`theta` 是圆的参数角。

`0.0` 表示从 0 弧度开始。

`2.0 * np.pi` 表示到 2π 弧度结束，也就是一整圈。

`num_points` 表示生成多少个角度点。

因为包含起点和终点，所以最后一个角度会回到一整圈的位置。

### 第 35 行

```python

```

这是空行，用来分隔角度生成和 x/y/z 计算。

### 第 36 行

```python
    x = center_x + radius * np.cos(theta)
```

计算每个轨迹点的 x 坐标。

圆的参数方程之一是：

```text
x = center_x + radius * cos(theta)
```

当 `theta` 从 0 到 2π 变化时，x 坐标会在圆心左右变化。

### 第 37 行

```python
    y = center_y + radius * np.sin(theta)
```

计算每个轨迹点的 y 坐标。

圆的参数方程之一是：

```text
y = center_y + radius * sin(theta)
```

当 `theta` 从 0 到 2π 变化时，y 坐标会在圆心上下变化。

### 第 38 行

```python
    z = np.full_like(theta, center_z)
```

生成每个轨迹点的 z 坐标。

`np.full_like(theta, center_z)` 的意思是：生成一个和 `theta` 长度一样的数组，里面每个值都是 `center_z`。

所以这个圆是在固定高度上画的。

也就是说，z 不变，只改变 x 和 y。

### 第 39 行

```python

```

这是空行，用来分隔坐标计算和返回结果。

### 第 40 行

```python
    return np.column_stack((x, y, z))
```

把 `x`、`y`、`z` 三个数组合并成一个二维数组。

每一行是一个点：

```text
[x, y, z]
```

最终返回的形状类似：

```text
[
  [x0, y0, z0],
  [x1, y1, z1],
  [x2, y2, z2],
  ...
]
```

### 第 41 行

```python

```

这是空行。

### 第 42 行

```python

```

这是第二个空行。

用于分隔两个顶层函数。

### 第 43 行

```python
def summarize_points(points: np.ndarray) -> dict[str, np.ndarray | float]:
```

定义一个函数，名字是 `summarize_points`。

它用于检查和总结轨迹点。

参数 `points` 应该是 numpy 数组。

返回值是一个字典，字典里的值可能是 numpy 数组，也可能是浮点数。

### 第 44 行

```python
    """Return basic checks for a generated trajectory."""
```

这是函数说明。

意思是：返回生成轨迹的一些基础检查结果。

### 第 45 行

```python
    if points.ndim != 2 or points.shape[1] != 3:
```

检查 `points` 的形状是否正确。

`points.ndim != 2` 表示它不是二维数组。

`points.shape[1] != 3` 表示每个点不是 3 个数。

正确格式应该是：

```text
N 行，3 列
```

也就是：

```text
[x, y, z]
```

### 第 46 行

```python
        raise ValueError("points must have shape (N, 3)")
```

如果轨迹点格式不对，就主动报错。

错误信息是：

```text
points must have shape (N, 3)
```

### 第 47 行

```python

```

这是空行，用来分隔格式检查和后面的计算。

### 第 48 行

```python
    first_point = points[0]
```

取出第一个轨迹点。

`points[0]` 表示数组里的第一行。

### 第 49 行

```python
    last_point = points[-1]
```

取出最后一个轨迹点。

`points[-1]` 表示数组里的最后一行。

### 第 50 行

```python
    closed_error = float(np.linalg.norm(first_point - last_point))
```

计算起点和终点之间的距离。

`first_point - last_point` 会得到两个点的坐标差。

`np.linalg.norm(...)` 会计算这个差值向量的长度。

如果轨迹完全闭合，这个值应该接近 0。

`float(...)` 把 numpy 的数值转换成普通 Python 浮点数。

### 第 51 行

```python

```

这是空行，用来分隔计算和返回结果。

### 第 52 行

```python
    return {
```

开始返回一个字典。

字典用于把多个检查结果打包返回。

### 第 53 行

```python
        "first_point": first_point,
```

字典里保存第一个轨迹点。

键名是 `"first_point"`。

### 第 54 行

```python
        "last_point": last_point,
```

字典里保存最后一个轨迹点。

键名是 `"last_point"`。

### 第 55 行

```python
        "min_xyz": points.min(axis=0),
```

计算所有轨迹点在 x、y、z 三个方向上的最小值。

`axis=0` 表示按列计算。

结果类似：

```text
[最小 x, 最小 y, 最小 z]
```

### 第 56 行

```python
        "max_xyz": points.max(axis=0),
```

计算所有轨迹点在 x、y、z 三个方向上的最大值。

结果类似：

```text
[最大 x, 最大 y, 最大 z]
```

### 第 57 行

```python
        "closed_error": closed_error,
```

把闭合误差保存到字典里。

键名是 `"closed_error"`。

### 第 58 行

```python
    }
```

字典结束。

函数返回这个字典。

## 3. plot_trajectory.py

这个文件负责把轨迹画出来。

它不会生成轨迹，也不会控制机械臂。

### 第 1 行

```python
"""Plot local trajectories before connecting to a robot."""
```

这是文件说明。

意思是：在连接机器人之前，先在本地画出轨迹。

### 第 2 行

```python

```

这是空行，用来分隔文件说明和导入语句。

### 第 3 行

```python
from __future__ import annotations
```

启用更灵活的类型标注处理。

这里主要服务于后面的类型提示。

### 第 4 行

```python

```

这是空行，用来分隔导入语句。

### 第 5 行

```python
import os
```

导入 Python 标准库 `os`。

这里用它来设置环境变量 `MPLCONFIGDIR`。

### 第 6 行

```python
from pathlib import Path
```

从标准库 `pathlib` 导入 `Path`。

`Path` 用来更方便地处理文件路径。

### 第 7 行

```python

```

这是空行，用来分隔导入和路径配置。

### 第 8 行

```python
_MPL_CONFIG_DIR = Path(__file__).resolve().parent / ".matplotlib-cache"
```

定义 matplotlib 的缓存目录。

`__file__` 表示当前这个 Python 文件的路径。

`Path(__file__).resolve()` 把当前文件路径转换成绝对路径。

`.parent` 表示当前文件所在的文件夹。

`/ ".matplotlib-cache"` 表示在当前项目目录下拼出一个名为 `.matplotlib-cache` 的目录。

变量名前面的 `_` 表示这是模块内部使用的变量。

### 第 9 行

```python
_MPL_CONFIG_DIR.mkdir(exist_ok=True)
```

创建 `.matplotlib-cache` 目录。

`exist_ok=True` 表示如果这个目录已经存在，就不要报错。

这行是为了解决 matplotlib 默认缓存目录不可写的问题。

### 第 10 行

```python
os.environ.setdefault("MPLCONFIGDIR", str(_MPL_CONFIG_DIR))
```

设置环境变量 `MPLCONFIGDIR`。

`MPLCONFIGDIR` 告诉 matplotlib 把配置和缓存放在哪里。

`setdefault` 的意思是：如果这个环境变量还没有设置，就设置成我们指定的值；如果已经设置过，就保持原来的值。

`str(_MPL_CONFIG_DIR)` 把路径对象转换成字符串。

### 第 11 行

```python

```

这是空行，用来分隔 matplotlib 配置和第三方库导入。

### 第 12 行

```python
import matplotlib.pyplot as plt
```

导入 matplotlib 的绘图接口，并简写成 `plt`。

后面用它来创建图、显示图和保存图。

### 第 13 行

```python
import numpy as np
```

导入 numpy，并简写成 `np`。

这里主要是为了给函数参数写类型提示 `np.ndarray`。

### 第 14 行

```python

```

这是空行，用来分隔导入语句和函数定义。

### 第 15 行

```python

```

这是第二个空行。

用于符合 Python 顶层函数之间的常见代码风格。

### 第 16 行

```python
def plot_xy_trajectory(
```

开始定义绘图函数。

函数名是 `plot_xy_trajectory`。

意思是：绘制轨迹在 x-y 平面上的投影。

### 第 17 行

```python
    points: np.ndarray,
```

定义第一个参数 `points`。

它应该是 numpy 数组。

数组里每一行是一个轨迹点 `[x, y, z]`。

### 第 18 行

```python
    title: str,
```

定义第二个参数 `title`。

它是图的标题。

`str` 表示字符串。

### 第 19 行

```python
    output_path: str | Path | None = None,
```

定义第三个参数 `output_path`。

它表示图片保存路径。

它可以是字符串，可以是 `Path` 对象，也可以是 `None`。

默认值是 `None`，表示默认不保存。

### 第 20 行

```python
    show: bool = False,
```

定义第四个参数 `show`。

它表示是否弹出 matplotlib 图形窗口。

默认是 `False`，表示不弹窗，只保存图。

### 第 21 行

```python
) -> None:
```

结束函数参数列表。

`-> None` 表示这个函数不返回值。

它的作用是画图和保存图。

### 第 22 行

```python
    """Plot the x-y projection of a trajectory."""
```

这是函数说明。

意思是：画出轨迹在 x-y 平面上的投影。

### 第 23 行

```python
    if points.ndim != 2 or points.shape[1] != 3:
```

检查传进来的轨迹点格式是否正确。

正确格式应该是二维数组，并且每行有 3 个数。

也就是：

```text
[x, y, z]
```

### 第 24 行

```python
        raise ValueError("points must have shape (N, 3)")
```

如果轨迹点格式不正确，就报错。

这样可以避免画图时出现难理解的问题。

### 第 25 行

```python

```

这是空行，用来分隔格式检查和绘图代码。

### 第 26 行

```python
    fig, ax = plt.subplots(figsize=(6, 6))
```

创建一张图和一个坐标轴。

`fig` 表示整张图。

`ax` 表示图中的坐标区域。

`figsize=(6, 6)` 表示图片宽 6 英寸、高 6 英寸。

这样保存出来的图接近正方形，适合看圆。

### 第 27 行

```python
    ax.plot(points[:, 0], points[:, 1], marker=".", markersize=3, linewidth=1.5)
```

画轨迹线。

`points[:, 0]` 表示所有点的第 0 列，也就是所有 x 坐标。

`points[:, 1]` 表示所有点的第 1 列，也就是所有 y 坐标。

`marker="."` 表示每个轨迹点用小点标出来。

`markersize=3` 表示点的大小。

`linewidth=1.5` 表示连线宽度。

### 第 28 行

```python
    ax.scatter(points[0, 0], points[0, 1], color="green", label="start", zorder=3)
```

用绿色点标出起点。

`points[0, 0]` 是第一个点的 x 坐标。

`points[0, 1]` 是第一个点的 y 坐标。

`label="start"` 表示图例里显示为 start。

`zorder=3` 表示这个点画在较上层，避免被轨迹线盖住。

### 第 29 行

```python
    ax.scatter(points[-1, 0], points[-1, 1], color="red", label="end", zorder=3)
```

用红色点标出终点。

`points[-1, 0]` 是最后一个点的 x 坐标。

`points[-1, 1]` 是最后一个点的 y 坐标。

如果轨迹闭合，红色终点应该和绿色起点重合或非常接近。

### 第 30 行

```python

```

这是空行，用来分隔画轨迹和设置图形样式。

### 第 31 行

```python
    ax.set_title(title)
```

设置图的标题。

标题来自函数参数 `title`。

### 第 32 行

```python
    ax.set_xlabel("x / m")
```

设置 x 轴标签。

`x / m` 表示 x 坐标，单位是米。

### 第 33 行

```python
    ax.set_ylabel("y / m")
```

设置 y 轴标签。

`y / m` 表示 y 坐标，单位是米。

### 第 34 行

```python
    ax.axis("equal")
```

让 x 轴和 y 轴使用相同的比例。

这很重要。

如果不设置，圆可能在图上看起来像椭圆。

### 第 35 行

```python
    ax.grid(True)
```

打开网格线。

网格线方便观察轨迹范围和形状。

### 第 36 行

```python
    ax.legend()
```

显示图例。

图例会显示 start 和 end。

### 第 37 行

```python

```

这是空行，用来分隔图形样式和保存逻辑。

### 第 38 行

```python
    if output_path is not None:
```

判断是否需要保存图片。

如果 `output_path` 不是 `None`，说明用户给了保存路径。

### 第 39 行

```python
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
```

保存图片。

`output_path` 是保存路径。

`dpi=150` 表示图片清晰度。

`bbox_inches="tight"` 表示保存时尽量裁掉多余空白。

### 第 40 行

```python

```

这是空行，用来分隔保存逻辑和显示逻辑。

### 第 41 行

```python
    if show:
```

判断是否要尝试弹出图形窗口。

如果运行时加了 `--show`，这里就是 True。
但程序还会继续判断当前 matplotlib 后端是不是交互式后端。

### 第 42 行

```python
        backend = plt.get_backend().lower()
```

读取当前 matplotlib 后端名字，并转成小写。

这样后面就能判断它是不是像 `qt`、`tk` 这种能弹窗口的后端。

### 第 43 行

```python
        interactive_backends = ("qt", "tk", "gtk", "wx", "macosx", "nbagg", "ipympl")
```

定义一组交互式后端名字。

只要当前后端名字里包含这些字符串之一，就认为它可以尝试打开窗口。

### 第 44 行

```python
        if any(name in backend for name in interactive_backends):
```

检查当前后端是不是交互式后端。

`any(...)` 的意思是：只要后端名字里包含这些候选名字中的任意一个，就返回 True。

### 第 45 行

```python
            plt.show()
```

如果当前后端支持交互显示，就真正弹出 matplotlib 窗口。

### 第 46 行

```python
        else:
```

如果当前后端不支持弹窗，就走这里。

### 第 47 行

```python
            print(
```

打印一条提示信息。

### 第 48 行

```python
                f"[info] matplotlib backend '{plt.get_backend()}' is non-interactive; "
```

打印当前后端名字，并说明它不是交互式后端。

### 第 49 行

```python
                "skipping window display."
```

继续打印提示，说明程序会跳过窗口显示。

### 第 50 行

```python
            )
```

结束 `print()` 调用。

### 第 51 行

```python

```

这是空行，用来分隔显示逻辑和关闭图形资源。

### 第 52 行

```python
    plt.close(fig)
```

关闭这张图。

这样可以释放内存和图形资源。

如果以后批量生成很多图片，这一步很重要。

## 4. main.py

这个文件是程序入口。

你在命令行运行的就是它：

```bash
python main.py --shape circle
```

它负责读取命令行参数、调用轨迹生成函数、调用画图函数，并打印检查结果。

### 第 1 行

```python
"""Generate and plot local drawing trajectories.
```

这是文件说明的第一行。

意思是：生成并绘制本地绘图轨迹。

### 第 2 行

```python

```

这是文件说明里的空行。

### 第 3 行

```python
This program is for local validation only. It does not connect to the Flexiv
```

这是文件说明的一部分。

意思是：这个程序只用于本地验证。

它不会连接 Flexiv 机械臂。

### 第 4 行

```python
robot and does not send any robot motion command.
```

这是文件说明的继续。

意思是：它不会发送任何机器人运动命令。

这句很重要，说明当前代码是安全的本地仿真/验证代码。

### 第 5 行

```python
"""
```

文件说明结束。

### 第 6 行

```python

```

这是空行，用来分隔文件说明和导入语句。

### 第 7 行

```python
from __future__ import annotations
```

启用更灵活的类型标注处理。

这里主要是为了配合现代 Python 类型提示。

### 第 8 行

```python

```

这是空行，用来分隔不同导入。

### 第 9 行

```python
import argparse
```

导入 Python 标准库 `argparse`。

`argparse` 用来解析命令行参数。

例如解析：

```bash
--shape circle
--radius 0.03
--points 120
```

### 第 10 行

```python

```

这是空行，用来分隔标准库导入和自己项目里的导入。

### 第 11 行

```python
from config import CIRCLE_CENTER, CIRCLE_POINTS, CIRCLE_RADIUS, DEFAULT_OUTPUT
```

从 `config.py` 导入默认配置。

导入的内容包括：

```text
CIRCLE_CENTER：圆心
CIRCLE_POINTS：点数
CIRCLE_RADIUS：半径
DEFAULT_OUTPUT：默认图片名
```

### 第 12 行

```python
from plot_trajectory import plot_xy_trajectory
```

从 `plot_trajectory.py` 导入绘图函数。

这个函数负责把轨迹画出来并保存图片。

### 第 13 行

```python
from trajectory import generate_circle, summarize_points
```

从 `trajectory.py` 导入两个函数：

```text
generate_circle：生成圆形轨迹
summarize_points：检查和总结轨迹点
```

### 第 14 行

```python

```

这是空行，用来分隔导入语句和函数定义。

### 第 15 行

```python

```

这是第二个空行。

用于符合 Python 顶层函数之间的常见代码风格。

### 第 16 行

```python
def parse_args() -> argparse.Namespace:
```

定义一个函数，名字是 `parse_args`。

它负责读取命令行参数。

`-> argparse.Namespace` 表示这个函数返回一个 `argparse.Namespace` 对象。

这个对象里会保存用户输入的参数。

### 第 17 行

```python
    parser = argparse.ArgumentParser(
```

创建一个命令行参数解析器。

变量名是 `parser`。

后面会用它来定义程序支持哪些参数。

这一行参数没写完，下一行继续。

### 第 18 行

```python
        description="Generate a local trajectory for robot drawing."
```

给命令行程序加一段说明。

当你运行：

```bash
python main.py --help
```

会看到这段说明。

### 第 19 行

```python
    )
```

结束 `ArgumentParser` 的创建。

### 第 20 行

```python
    parser.add_argument(
```

开始添加一个命令行参数。

这里添加的是 `--shape` 参数。

### 第 21 行

```python
        "--shape",
```

定义参数名字是 `--shape`。

用户可以这样写：

```bash
python main.py --shape circle
```

### 第 22 行

```python
        choices=("circle",),
```

限制 `--shape` 只能选择 `"circle"`。

现在只支持圆形，所以这里只有一个选项。

注意 `("circle",)` 是只有一个元素的元组，逗号不能少。

### 第 23 行

```python
        default="circle",
```

设置默认值。

如果用户不写 `--shape`，默认就是 `"circle"`。

### 第 24 行

```python
        help="Trajectory shape to generate. Currently only circle is supported.",
```

设置这个参数的帮助说明。

当运行 `python main.py --help` 时会显示。

### 第 25 行

```python
    )
```

结束 `--shape` 参数的定义。

### 第 26 行

```python
    parser.add_argument(
```

开始添加第二个命令行参数。

这里添加的是 `--radius`。

### 第 27 行

```python
        "--radius",
```

定义参数名字是 `--radius`。

用户可以这样写：

```bash
python main.py --radius 0.02
```

### 第 28 行

```python
        type=float,
```

指定 `--radius` 的类型是浮点数。

也就是说，用户输入的文本会被转换成 `float`。

例如 `"0.02"` 会变成数字 `0.02`。

### 第 29 行

```python
        default=CIRCLE_RADIUS,
```

设置默认半径。

默认值来自 `config.py` 里的 `CIRCLE_RADIUS`。

当前是 `0.03` 米。

### 第 30 行

```python
        help="Circle radius in meters.",
```

设置 `--radius` 的帮助说明。

意思是：圆半径，单位是米。

### 第 31 行

```python
    )
```

结束 `--radius` 参数的定义。

### 第 32 行

```python
    parser.add_argument(
```

开始添加第三个命令行参数。

这里添加的是 `--points`。

### 第 33 行

```python
        "--points",
```

定义参数名字是 `--points`。

用户可以这样写：

```bash
python main.py --points 200
```

### 第 34 行

```python
        type=int,
```

指定 `--points` 的类型是整数。

例如 `"200"` 会被转换成整数 `200`。

### 第 35 行

```python
        default=CIRCLE_POINTS,
```

设置默认点数。

默认值来自 `config.py` 里的 `CIRCLE_POINTS`。

当前是 `120`。

### 第 36 行

```python
        help="Number of generated points.",
```

设置 `--points` 的帮助说明。

意思是：生成多少个轨迹点。

### 第 37 行

```python
    )
```

结束 `--points` 参数的定义。

### 第 38 行

```python
    parser.add_argument(
```

开始添加第四个命令行参数。

这里添加的是 `--output`。

### 第 39 行

```python
        "--output",
```

定义参数名字是 `--output`。

用户可以这样写：

```bash
python main.py --output my_circle.png
```

### 第 40 行

```python
        default=DEFAULT_OUTPUT,
```

设置默认输出文件名。

默认值来自 `config.py` 里的 `DEFAULT_OUTPUT`。

当前是：

```text
circle_trajectory.png
```

### 第 41 行

```python
        help="Path of the saved trajectory image.",
```

设置 `--output` 的帮助说明。

意思是：保存轨迹图片的路径。

### 第 42 行

```python
    )
```

结束 `--output` 参数的定义。

### 第 43 行

```python
    parser.add_argument(
```

开始添加第五个命令行参数。

这里添加的是 `--show`。

### 第 44 行

```python
        "--show",
```

定义参数名字是 `--show`。

用户可以这样写：

```bash
python main.py --show
```

### 第 45 行

```python
        action="store_true",
```

指定 `--show` 是一个开关参数。

如果用户写了 `--show`，它的值就是 `True`。

如果用户没写，默认就是 `False`。

### 第 46 行

```python
        help="Show the matplotlib window in addition to saving the image.",
```

设置 `--show` 的帮助说明。

意思是：除了保存图片，也尝试显示 matplotlib 图形窗口。

### 第 47 行

```python
    )
```

结束 `--show` 参数的定义。

### 第 48 行

```python
    return parser.parse_args()
```

解析命令行参数，并把结果返回。

例如运行：

```bash
python main.py --shape circle --radius 0.02
```

返回对象里会有：

```text
args.shape = "circle"
args.radius = 0.02
```

### 第 49 行

```python

```

这是空行。

### 第 50 行

```python

```

这是第二个空行。

用于分隔两个顶层函数。

### 第 51 行

```python
def main() -> None:
```

定义主函数。

主函数负责组织整个程序流程。

`-> None` 表示它不返回值。

### 第 52 行

```python
    args = parse_args()
```

调用 `parse_args()` 读取命令行参数。

返回结果保存到变量 `args`。

后面可以用：

```text
args.shape
args.radius
args.points
args.output
args.show
```

### 第 53 行

```python

```

这是空行，用来分隔参数解析和轨迹生成逻辑。

### 第 54 行

```python
    if args.shape == "circle":
```

判断用户选择的轨迹形状是不是圆形。

当前程序只支持 `"circle"`。

### 第 55 行

```python
        points = generate_circle(
```

调用 `generate_circle` 函数生成圆形轨迹。

生成出来的轨迹点保存到变量 `points`。

函数参数比较多，所以分多行写。

### 第 56 行

```python
            center=CIRCLE_CENTER,
```

把圆心传给 `generate_circle`。

圆心来自 `config.py` 里的 `CIRCLE_CENTER`。

### 第 57 行

```python
            radius=args.radius,
```

把半径传给 `generate_circle`。

半径来自命令行参数 `args.radius`。

如果用户没有指定，就使用默认半径 `0.03`。

### 第 58 行

```python
            num_points=args.points,
```

把点数传给 `generate_circle`。

点数来自命令行参数 `args.points`。

如果用户没有指定，就使用默认点数 `120`。

### 第 59 行

```python
        )
```

结束 `generate_circle(...)` 函数调用。

### 第 60 行

```python
        title = "Circle TCP trajectory preview"
```

设置图的标题。

这个标题会显示在保存的图片上方。

`TCP trajectory` 表示这是机械臂末端 TCP 的轨迹预览。

### 第 61 行

```python
    else:
```

如果 `args.shape` 不是 `"circle"`，就执行这里。

目前由于 `argparse` 已经限制只能选 `"circle"`，正常情况下不会走到这里。

这行是为了让代码以后扩展方形时结构更清楚。

### 第 62 行

```python
        raise ValueError(f"unsupported shape: {args.shape}")
```

如果遇到不支持的形状，就主动报错。

`f"..."` 是格式化字符串，可以把 `args.shape` 的实际值放进错误信息。

### 第 63 行

```python

```

这是空行，用来分隔轨迹生成和轨迹检查/画图。

### 第 64 行

```python
    summary = summarize_points(points)
```

调用 `summarize_points` 检查轨迹点。

检查结果保存到变量 `summary`。

里面包括：

```text
first_point
last_point
min_xyz
max_xyz
closed_error
```

### 第 65 行

```python
    plot_xy_trajectory(points, title=title, output_path=args.output, show=args.show)
```

调用绘图函数，把轨迹画出来。

传入的内容包括：

```text
points：轨迹点
title：图标题
output_path：保存路径
show：是否显示窗口
```

默认会保存到 `circle_trajectory.png`。
在当前 WSL 环境里，`--show` 只是“尝试显示窗口”，如果后端不是交互式的，就会跳过弹窗。

### 第 66 行

```python

```

这是空行，用来分隔画图和打印结果。

### 第 67 行

```python
    print(f"shape: {args.shape}")
```

打印轨迹形状。

当前会输出：

```text
shape: circle
```

### 第 68 行

```python
    print(f"point count: {len(points)}")
```

打印轨迹点数量。

`len(points)` 表示 `points` 里有多少行。

当前默认是 120。

### 第 69 行

```python
    print(f"center xyz / m: {CIRCLE_CENTER}")
```

打印圆心坐标。

`/ m` 表示单位是米。

### 第 70 行

```python
    print(f"radius / m: {args.radius}")
```

打印圆半径。

`args.radius` 是实际使用的半径。

### 第 71 行

```python
    print(f"first point: {summary['first_point']}")
```

打印第一个轨迹点。

`summary['first_point']` 从检查结果字典里取出起点。

### 第 72 行

```python
    print(f"last point: {summary['last_point']}")
```

打印最后一个轨迹点。

`summary['last_point']` 从检查结果字典里取出终点。

### 第 73 行

```python
    print(f"min xyz: {summary['min_xyz']}")
```

打印 x、y、z 三个方向上的最小值。

这可以帮助你检查轨迹范围有没有太大。

### 第 74 行

```python
    print(f"max xyz: {summary['max_xyz']}")
```

打印 x、y、z 三个方向上的最大值。

这也用于检查轨迹范围。

### 第 75 行

```python
    print(f"closed error / m: {summary['closed_error']:.12f}")
```

打印闭合误差。

`summary['closed_error']` 是起点和终点之间的距离。

`:.12f` 表示保留 12 位小数显示。

如果轨迹闭合，这个值应该非常接近 0。

### 第 76 行

```python
    print(f"saved plot: {args.output}")
```

打印图片保存位置。

如果使用默认设置，会输出：

```text
saved plot: circle_trajectory.png
```

### 第 77 行

```python

```

这是空行。

### 第 78 行

```python

```

这是第二个空行。

用于分隔主函数和程序入口判断。

### 第 79 行

```python
if __name__ == "__main__":
```

这是 Python 常见的程序入口判断。

意思是：只有当这个文件被直接运行时，才执行下面的代码。

例如：

```bash
python main.py
```

会满足这个条件。

如果别的文件只是 `import main`，则不会自动运行下面的 `main()`。

### 第 80 行

```python
    main()
```

调用主函数 `main()`。

这行真正启动整个程序流程：

```text
读取命令行参数
生成圆形轨迹
检查轨迹
保存图片
打印结果
```

## 5. 当前程序运行流程总结

当你运行：

```bash
cd /home/yoyo/projects/test
source .venv/bin/activate
python main.py --shape circle
```

程序大致按这个顺序执行：

```text
1. main.py 被启动
2. 执行 main()
3. parse_args() 读取命令行参数
4. generate_circle() 生成圆形轨迹点
5. summarize_points() 检查轨迹范围和闭合误差
6. plot_xy_trajectory() 保存轨迹图
7. print() 打印检查结果
```

当前生成的轨迹点格式是：

```text
[x, y, z]
```

当前还没有：

```text
姿态 qw / qx / qy / qz
Flexiv RDK
robot_control.py
真实机械臂运动命令
```

这些内容等本地圆形和方形轨迹都确认正确后，再逐步加入。
