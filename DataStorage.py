import requests

import mysql.connector
from mysql.connector import Error

if __name__ == '__main__':
    # 正确接口地址（根据页面中的 /jx_plates 推断）
    jx_plates_url =

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.142 Safari/537.36",
            "Referer": ,  # 必须与页面 URL 一致
            "Accept": "application/json",
        }
        response = requests.get(jx_plates_url, headers=headers)

        # 调试输出
        print("状态码:", response.status_code)
        print("响应内容:", response.text[:100])  # 查看片段

        # 解析 JSON
        data = response.json()
        print("精选板块数据:", data)

    except Exception as e:
        print("请求失败:", e)

    try:
        # 连接 MySQL
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="stock"
        )

        cursor = conn.cursor()

        # 插入数据 (使用 %s 占位符)
        insert_sql = """
        INSERT INTO stock_plates (
            plate_code, plate_name, strength, change_rate, speed, turnover,
            net_inflow, main_buy, main_sell, quantity_ratio, market_value,
            field12, field13, field14, field15, field16, field17, field18
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 批量插入
        values = [item[:18] for item in data]
        cursor.executemany(insert_sql, values)
        conn.commit()

        print(f"成功插入 {cursor.rowcount} 条数据")

    except Error as e:
        print("MySQL 错误:", e)
        conn.rollback()

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()