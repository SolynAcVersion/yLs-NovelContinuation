from os import error
import sqlite3 as sql
import json
from typing import Optional, Dict, List, Any, Union


class NovelDB:
    """
    novel analyzing database manager
    provideing CRUD operation interfaces
    """

    def __init__(self, db_path: str):
        # db_path: path of the local database
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self) -> bool:
        try:
            self.conn = sql.connect(self.db_path)
            self.conn.row_factory = sql.Row
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"数据库读取出错：{e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def _record_exists(self, table_name: str, record_id: Union[str, int]) -> bool:
        try:
            _sql = f"SELECT COUNT(*) as count FROM {table_name} WHERE id = ?"
            self.cursor.execute(_sql, (record_id,))
            res = self.cursor.fetchone()
            return res["count"] > 0
        except Exception as e:
            print(f"检查存在失败：{e}")
            return False

    def create_new_table(self) -> bool:
        """
        create new table for the new book waiting to be analyzed
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    core_personality TEXT,
                    development_trajectory TEXT,
                    relationship_network TEXT

                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS plot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timeline TEXT,
                    foreshadowing TEXT,
                    rhythm_analysis TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS style (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    narrative_perspective TEXT,
                    vocabulary_analysis TEXT,
                    sentence_pattern TEXT,
                    description_mode TEXT,
                    rhythm_control TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS ai_summary (
                    id TEXT PRIMARY KEY,
                    content TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.conn.commit()
            print("创建成功")
            return True

        except Exception as e:
            print(f"创建失败：{e}")
            self.conn.rollback()
            return False

    def add(self, table_name: str, data: Dict[str, Any]) -> bool:
        try:
            if table_name not in ["characters", "plot", "style", "ai_summary"]:
                print(f"不支持的表名：{table_name}")
                return False
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            values = list(data.values())

            sql_ = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql_, values)

            self.conn.commit()

            if table_name in ["characters", "ai_summary"]:
                inserted_id = data.get("id")
            else:
                inserted_id = self.cursor.lastrowid

            print(f"成功添加到{table_name}, ID: {inserted_id}")
            return True

        except sql.IntegrityError as e:
            print("添加失败！主键冲突！")
            self.conn.rollback()
            return False
        except Exception as e:
            print(f"添加失败！{e}")
            self.conn.rollback()
            return False

    def read(
        self, table_name: str, record_id: Optional[Union[str, int]] = None
    ) -> Optional[Union[List[Dict], dict]]:
        try:
            if table_name not in ["characters", "plot", "style", "ai_summary"]:
                print(f"不支持的表名：{table_name}")
                return None
            if record_id is None:
                sql_ = f"SELECT * FROM {table_name}"
                self.cursor.execute(sql_)
                rows = self.cursor.fetchall()

                res = [dict(row) for row in rows]
                print(f"从{table_name} 读取了 {len(res)} 条记录")
                return res
            else:
                sql_ = f"SELECT * FROM {table_name} WHERE id = ?"
                self.cursor.execute(sql_, (record_id,))
                row = self.cursor.fetchone()

                if row:
                    res = dict(row)
                    print(f"从{table_name}读取记录：{record_id}")
                    return res
                else:
                    print(f"记录不存在！{table_name}/{record_id}")
                    return None
        except Exception as e:
            print(f"读取失败！{e}")
            return None

    def update(
        self, table_name: str, record_id: Union[int, str], data: Dict[str, Any]
    ) -> bool:
        try:
            if table_name not in ["characters", "plot", "style", "ai_summary"]:
                print(f"不支持的表名：{table_name}")
                return False
            if not self._record_exists(table_name, record_id):
                print(f"记录不存在：{table_name}/{record_id}")
                return False

            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            values = list(data.values())
            values.append(record_id)

            sql_ = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"

            self.cursor.execute(sql_, values)
            self.conn.commit()

            print(f"更新成功！{table_name}/{record_id}")
            return True

        except Exception as e:
            print(f"更新失败！{e}")
            self.conn.rollback()
            return False
