#!/usr/bin/env python3
"""
Demo 1: NumPy Fundamentals - Memory Layout, Speed Benchmark & Broadcasting
==========================================================================
Story Anchor: 'NumPy is the power tool in the woodshop.'
Topics Covered:
  - Vectorization vs Python loops (speed benchmark)
  - 1D, 2D, 3D Array creation & memory strides
  - Slicing, Copy vs View mechanics
  - Broadcasting rules across mismatched dimensions
  - Boolean masking & conditional filtering
"""

import time
import numpy as np

def header(title: str):
    print(f"\n{'='*70}\n[NUMPY DEMO] {title}\n{'='*70}")

def benchmark_speed():
    header("1. Vectorization vs Python Pure Loop Benchmark")
    size = 1_000_000
    py_list_a = list(range(size))
    py_list_b = list(range(size))
    
    # 1. Pure Python loop
    start = time.perf_counter()
    py_result = [a + b for a, b in zip(py_list_a, py_list_b)]
    py_duration = time.perf_counter() - start
    
    # 2. NumPy Vectorized
    np_arr_a = np.arange(size, dtype=np.int64)
    np_arr_b = np.arange(size, dtype=np.int64)
    start = time.perf_counter()
    np_result = np_arr_a + np_arr_b
    np_duration = time.perf_counter() - start
    
    speedup = py_duration / np_duration
    print(f"Elements processed: {size:,}")
    print(f"Pure Python List Comprehension: {py_duration*1000:.2f} ms")
    print(f"NumPy Vectorized Addition     : {np_duration*1000:.2f} ms")
    print(f"-> Speedup Factor: {speedup:.1f}x FASTER!")
    assert np_result[500] == py_result[500]

def array_shapes_and_strides():
    header("2. Shapes, Dimensions & Memory Strides (1D -> 2D -> 3D)")
    arr_1d = np.arange(12, dtype=np.int32)
    print("1D Array:")
    print(f"  Shape: {arr_1d.shape}, Dtype: {arr_1d.dtype}, Itemsize: {arr_1d.itemsize} bytes, Strides: {arr_1d.strides}")
    print(f"  Data: {arr_1d}")
    
    arr_2d = arr_1d.reshape(3, 4)
    print("\nReshaped to 2D Array (3 rows x 4 cols):")
    print(f"  Shape: {arr_2d.shape}, Strides: {arr_2d.strides} (Row step 16 bytes, Col step 4 bytes)")
    print(f"  Data:\n{arr_2d}")
    
    arr_3d = arr_1d.reshape(2, 3, 2)
    print("\nReshaped to 3D Array (2 blocks x 3 rows x 2 cols):")
    print(f"  Shape: {arr_3d.shape}, Strides: {arr_3d.strides}")
    print(f"  Data:\n{arr_3d}")

def copy_vs_view():
    header("3. Critical Gotcha: Slicing Views vs Explicit Copies")
    orig = np.array([10, 20, 30, 40, 50])
    print(f"Original Array: {orig}")
    
    # Slicing creates a VIEW, NOT a copy!
    view_slice = orig[1:4]
    view_slice[0] = 999
    print("\nMutated view_slice[0] = 999:")
    print(f"  view_slice: {view_slice}")
    print(f"  Original after view mutation: {orig}  <-- NOTE: Original was modified!")
    
    # Safe explicit copy
    orig_copy = orig.copy()
    orig_copy[0] = -1
    print("\nMutated explicit copy orig_copy[0] = -1:")
    print(f"  orig_copy: {orig_copy}")
    print(f"  Original remains: {orig}  <-- NOTE: Original was preserved!")

def broadcasting_rules():
    header("4. Broadcasting Magic: Arithmetic Across Different Shapes")
    matrix = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]])  # Shape (3, 3)
    vector = np.array([10, 20, 30])  # Shape (3,)
    
    print(f"Matrix shape: {matrix.shape}")
    print(f"Vector shape: {vector.shape}")
    print("Broadcasting vector across rows of matrix:\n", matrix + vector)
    
    col_vector = np.array([[100], [200], [300]])  # Shape (3, 1)
    print(f"\nColumn Vector shape: {col_vector.shape}")
    print("Broadcasting column vector across columns of matrix:\n", matrix + col_vector)

def boolean_masking():
    header("5. Fast Filtering: Boolean Masking & Conditional Search")
    salaries = np.array([45000, 62000, 89000, 115000, 52000, 138000, 97000])
    mask = (salaries > 60000) & (salaries < 100000)
    
    print(f"Salaries: {salaries}")
    print(f"Mask ((salaries > 60k) & (salaries < 100k)): {mask}")
    print(f"Filtered results: {salaries[mask]}")
    
    # np.where for vectorized if-else
    tier = np.where(salaries >= 100000, "Senior", "Standard")
    print(f"Vectorized Classification via np.where:\n  {list(zip(salaries, tier))}")

if __name__ == "__main__":
    print("Running Demo 1: NumPy Deep Dive...")
    benchmark_speed()
    array_shapes_and_strides()
    copy_vs_view()
    broadcasting_rules()
    boolean_masking()
    print("\n[SUCCESS] Demo 1 completed cleanly!\n")

