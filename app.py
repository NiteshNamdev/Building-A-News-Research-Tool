import streamlit as st

st.title('Equity Research News Tool')
st.write('Enter your query to get the latest news articles summarized.')

query = st.text_input('Query')

if st.button('Get News'):
  if query:
    summaries = get_summary(query)
    response = llm_chain.run({'query': query, 'summaries': summaries})
    st.write('### Summary:')
    st.write(response)
  else:
    st.write('Please enter a query.')