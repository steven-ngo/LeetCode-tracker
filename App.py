from Service import *
from pathlib import Path
import altair as alt
import datetime
import sqlite3
import streamlit as st


st.set_page_config(
    page_title='LeetCode Tracker'
)

# App description
st.markdown('''
# LeetCode Tracker

- Source Code: https://github.com/steven-ngo/LeetCode-Tracker
- Language: `Python`
- Libraries: `streamlit` `altair` `pandas` `sqlite3`
''')
st.write('---')


IsDBExisted = Path('./leetcode.db').exists()

conn = sqlite3.connect('leetcode.db')

if not IsDBExisted:
   Service.initializeDB(conn)

data = Service.getData(conn)

topicOptions=[ 'Array',
               'String',
               'Hash Table',
               'Dynamic Programming',
               'Math',
               'Sorting',
               'Greedy',
               'Depth-First Search',
               'Binary Search',
               'Breadth-First Search',
               'Tree',
               'Matrix',
               'Bit Manipulation',
               'Two Pointers',
               'Binary Tree',
               'Heap',
               'Prefix Sum',
               'Stack',
               'Simulation',
               'Graph',
               'Design',
               'Counting',
               'Sliding Window',
               'Backtracking',
               'Linked List',
               'Trie',
               'Recursion',
               'Queue',
               'Binary Search Tree'
            ]
difficultyOptions = [ 'Easy', 'Medium', 'Hard']

st.info('Use the table below to add, remove, and edit items. Commit your changes when done.')

st.data_editor(
    data,
    disabled=['id','date'],
    num_rows='dynamic',
    column_config={
      'problem_name': st.column_config.TextColumn(
            max_chars=80,
            validate='^[a-zA-Z0-9+.~ ]',
            required=True,
        ),
        'topic': st.column_config.SelectboxColumn(
            options=topicOptions,
            required=True,
        ),
         'difficulty': st.column_config.SelectboxColumn(
            options=difficultyOptions,
            required=True,
        ),
         'link': st.column_config.LinkColumn(
            validate='^https://leetcode.com/problems/([-a-zA-Z0-9()@:%_\+.~#?&//=]*)',
            max_chars=100
        ),
      'note': st.column_config.TextColumn(
            max_chars=200,
            validate='^[a-zA-Z0-9+.~ ]'
        ),
      'date':  st.column_config.DateColumn(
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date(2005, 1, 1),
            format='MM.DD.YYYY',
            default=datetime.date.today(),
            step=1,
        ),
    }, 
    key='problem_table')


isChanged = any(len(value) for value in st.session_state.problem_table.values())

st.button(
    'Commit changes',
    type='primary',
    disabled=not isChanged,
    on_click=Service.update_data,
    args=(conn, data, st.session_state.problem_table))



st.subheader('Reports', divider='red')

topicReport = Service.getTopicReport(conn)

st.altair_chart(alt.Chart(topicReport)
    .mark_bar(orient='horizontal')
    .encode(
        x='number',
        y=alt.Y('topic').sort('-x'),
        
    ),
    use_container_width= True
   )


st.markdown('''---''')

difficultyReport = Service.getDifficultyReport(conn)

st.altair_chart(alt.Chart(difficultyReport)
    .mark_bar(orient='horizontal')
    .encode(
        x='number',
        y=alt.Y('difficulty').sort('-x'),
        
    ),
    use_container_width= True
   )
