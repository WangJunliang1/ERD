# -*- coding: utf-8 -*-

import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser(description='用于仿真画图的命令行工具')
    parser.add_argument('--input', '-i', type=str,
                        help='输入Excel文件的路径', required=True)
    parser.add_argument('--output', '-o', type=str,
                        help='输出图表的路径', required=True)
    args = parser.parse_args()
    print('abcd1233:', args.input)
    print('abcd12334:', args.output)
    
def chart_course():
    # 读取 Excel 文件
    excel_file_path = '/root/show.xlsx'
    df = pd.read_excel(excel_file_path)

    # 使用at方法通过行和列的标签读取元素值
    value_at_label = df.at[0, 'A']

    # 使用iat方法通过行和列的索引读取元素值
    value_at_index = df.iat[0, 1]

    print(value_at_label)
    print(value_at_index)


if __name__ == '__main__':
    chart_course()
