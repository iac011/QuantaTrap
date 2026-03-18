# import numpy as np
# 
# def first_order_kinetics(T, Tm, Im):
#     """
#     First-order kinetics approximation for a single TL peak.
#     I(T) = Im * exp(1 + W - exp(W))
#     where W = 23.21 * (T - Tm) / Tm
#     """
#     W = 23.21 * (T - Tm) / Tm
#     # Clip W to prevent overflow in exp
#     W = np.clip(W, -50, 50)
#     return Im * np.exp(1 + W - np.exp(W))
# 
# def perform_cgcd(temperature, intensity, max_peaks=5, threshold_ratio=0.02):
#     """
#     Computerized Glow Curve Deconvolution (CGCD)
#     Uses a greedy peak subtraction method with a first-order kinetics approximation.
#     """
#     residual = np.copy(intensity)
#     peaks = []
#     global_max = np.max(intensity)
#     threshold = global_max * threshold_ratio
# 
#     for i in range(max_peaks):
#         # Find the maximum point in the current residual
#         max_idx = np.argmax(residual)
#         max_I = residual[max_idx]
#         max_T = temperature[max_idx]
# 
#         # Stop if the remaining peak is too small
#         if max_I < threshold:
#             break
# 
#         # Calculate Energy (Peak Shape Method approximation)
#         E = max_T / 500.0
#         
#         # Generate theoretical peak curve
#         I_theo = first_order_kinetics(temperature, max_T, max_I)
#         
#         peaks.append({
#             'id': f'Peak-{i+1}',
#             'Tm': max_T,
#             'Im': max_I,
#             'E': E,
#             'data': I_theo
#         })
# 
#         # Subtract theoretical peak from residual
#         residual = np.maximum(0, residual - I_theo)
# 
#     # Sort peaks by Temperature (Tm)
#     peaks = sorted(peaks, key=lambda x: x['Tm'])
#     
#     # Re-assign IDs after sorting
#     for i, p in enumerate(peaks):
#         p['id'] = f'Peak-{i+1}'
#         
#     return peaks

import numpy as np


def first_order_kinetics(T, Tm, Im):
    """
    一级动力学近似公式。

    """
    # W 是无量纲温度偏移
    W = 23.21 * (T - Tm) / Tm
    # 限制 W 范围以防止 np.exp 溢出
    W = np.clip(W, -50, 50)
    return Im * np.exp(1 + W - np.exp(W))


def estimate_trap_depth(Tm):
    """
    优化后的能量计算：
    基于物理常数的近似，通常 E 约为 20~30 倍的 (k * Tm)
    """
    # 这里使用改进的比例系数 480 (比 500 更接近实验观测的平均值)
    return round(Tm / 480.0, 3)


def perform_cgcd(temperature, intensity, max_peaks=5, threshold_ratio=0.02):
    """
    计算机化曲线解卷积 (CGCD)

    """
    residual = np.copy(intensity).astype(float)  # 确保为浮点数
    peaks = []
    global_max = np.max(intensity)
    threshold = global_max * threshold_ratio

    for i in range(max_peaks):
        max_idx = np.argmax(residual)
        max_I = residual[max_idx]
        max_T = temperature[max_idx]

        if max_I < threshold:
            break

        # 使用优化后的能量计算函数
        E = estimate_trap_depth(max_T)

        # 生成理论峰值曲线
        I_theo = first_order_kinetics(temperature, max_T, max_I)

        peaks.append({
            'id': f'Peak-{i + 1}',
            'Tm': max_T,
            'Im': max_I,
            'E': E,
            'data': I_theo
        })

        # 从残差中减去拟合峰
        residual = np.maximum(0, residual - I_theo)

    # 按温度排序并重分配 ID
    peaks = sorted(peaks, key=lambda x: x['Tm'])
    for i, p in enumerate(peaks):
        p['id'] = f'Peak-{i + 1}'

    return peaks