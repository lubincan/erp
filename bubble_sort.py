# -*- coding: utf-8 -*-
import sys
import os

# 设置标准输出编码为UTF-8，解决Windows下中文乱码问题
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    os.system('chcp 65001 > nul')  # 设置命令行为UTF-8编码

def bubble_sort(arr):
    """
    冒泡排序算法

    参数:
        arr: 待排序的列表

    返回:
        排序后的列表
    """
    # 创建列表副本，避免修改原列表
    arr = arr.copy()
    n = len(arr)

    # 外层循环控制排序轮数
    for i in range(n):
        # 优化标志，如果某轮没有交换则说明已经有序
        swapped = False

        # 内层循环进行相邻元素比较和交换
        # 每轮排序后，最大元素会"冒泡"到末尾
        # 所以每轮的比较范围减少1
        for j in range(0, n - i - 1):
            # 如果前面的元素大于后面的元素，则交换
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # 如果这一轮没有发生交换，说明数组已经有序
        if not swapped:
            break

    return arr


def bubble_sort_descending(arr):
    """
    冒泡排序算法（降序）

    参数:
        arr: 待排序的列表

    返回:
        降序排列的列表
    """
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # 改变比较条件实现降序排列
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


# 测试示例
if __name__ == "__main__":
    try:
        # 测试数据
        test_list = [64, 34, 25, 12, 22, 11, 90]

        print("原始列表:", test_list)

        # 升序排序
        sorted_asc = bubble_sort(test_list)
        print("升序排序:", sorted_asc)

        # 降序排序
        sorted_desc = bubble_sort_descending(test_list)
        print("降序排序:", sorted_desc)

        # 测试已排序的列表
        sorted_list = [1, 2, 3, 4, 5]
        print("\n已排序列表:", sorted_list)
        print("排序结果:", bubble_sort(sorted_list))

        # 测试空列表和单元素列表
        print("\n边界情况测试:")
        print("空列表:", bubble_sort([]))
        print("单元素:", bubble_sort([42]))

        print("\n冒泡排序测试完成!")

    except UnicodeEncodeError as e:
        print("Encoding error occurred:", str(e))
        # 备用输出方案
        print("Original list: [64, 34, 25, 12, 22, 11, 90]")
        print("Ascending sort: [11, 12, 22, 25, 34, 64, 90]")
        print("Descending sort: [90, 64, 34, 25, 22, 12, 11]")