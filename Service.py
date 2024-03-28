from collections import defaultdict
import pandas as pd
import streamlit as st


class Service:

    def initializeDB(conn):
        cursor = conn.cursor()

        cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS problems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    problem_name TEXT,
                    topic TEXT,
                    difficulty TEXT,
                    link TEXT,
                    note TEXT,
                    date TEXT
                )
                '''
            )

        cursor.execute(
                '''
                INSERT INTO problems
                    (problem_name, topic, difficulty, link, note, date)
                VALUES
                    ('1. Two Sum', 'Array', 'Easy', 'https://leetcode.com/problems/two-sum/', 'This is the first question', '2024-03-15'),
                    ('2. Add Two Numbers', 'Array', 'Easy', 'https://leetcode.com/problems/add-two-numbers/description/', 'This is the second question', '2024-03-25'),
                    ('3. Longest Substring Without Repeating', 'Array', 'Easy', 'https://leetcode.com/problems/longest-substring-without-repeating-characters', 'This is the third question', '2024-03-27')
                '''
            )

        conn.commit()


    def getData(conn):
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                '''
                SELECT * FROM problems;
                '''
            )

            data = cursor.fetchall()
        except:
            return None

        return  pd.DataFrame(data,  columns=['id','problem_name', 'topic', 'difficulty','link','note','date'])


    def update_data(conn, df, changes):
        cursor = conn.cursor()

        if changes['edited_rows']:
            deltas = st.session_state.problem_table['edited_rows']
            rows = []

            for i, delta in deltas.items():
                row_dict = df.iloc[i].to_dict()
                row_dict.update(delta)
                rows.append(row_dict)

            cursor.executemany(
                '''
                UPDATE problems
                SET
                    problem_name = :problem_name,
                    topic = :topic,
                    difficulty = :difficulty,
                    link = :link,
                    note = :note,
                    date = :date
                WHERE id = :id
                ''',
                rows,
            )

        if changes['added_rows']:
            cursor.executemany(
                '''
                INSERT INTO problems
                    (id, problem_name, topic, difficulty, link, note, date)
                VALUES
                    (:id, :problem_name, :topic, :difficulty, :link, :note, :date)
                ''',
                (defaultdict(lambda: None, row) for row in changes['added_rows']),
            )

        if changes['deleted_rows']:
            cursor.executemany(
                'DELETE FROM problems WHERE id = :id',
                ({'id': int(df.loc[i, 'id'])} for i in changes['deleted_rows'])
            )

        conn.commit()



    def getTopicReport(conn):
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT topic, COUNT(*) AS number
            FROM problems
            GROUP BY topic
            ORDER BY number DESC;
            '''
        )

        return pd.DataFrame(cursor.fetchall(),  columns=['topic','number']) 


    def getDifficultyReport(conn):
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT difficulty, COUNT(*) AS number
            FROM problems
            GROUP BY difficulty
            ORDER BY number DESC;
            '''
        )

        return pd.DataFrame(cursor.fetchall(),  columns=['difficulty','number']) 

