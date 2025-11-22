import streamlit as st
import requests

st.set_page_config(page_title="AI Search")

st.title(" AI Document Search Engine")
st.markdown("Search through the indexed 20 Newsgroups dataset (Space, Medicine, Graphics).")

# Input
query = st.text_input("Enter Query:", placeholder="Type something like 'nasa launch'...")
top_k = st.slider("Number of results", min_value=1, max_value=10, value=3)

if st.button("Search"):
    if not query:
        st.warning("Please enter a query first.")
    else:
        try:
            # Call the FastAPI backend
            res = requests.post(
                "http://127.0.0.1:8000/search", 
                json={"query": query, "top_k": top_k}
            )
            
            if res.status_code == 200:
                data = res.json()
                results = data.get("results", [])
                
                st.success(f"Found {len(results)} relevant documents.")
                
                # Display results nicely
                for item in results:
                    with st.container():
                        st.subheader(f" Document ID: {item['doc_id']}")
                        st.caption(f"Relevance Score: {item['score']}")
                        st.info(f"\"{item['preview']}\"")
                        
                        # Show explanation in a dropdown
                        with st.expander("See why this matched"):
                            st.write("**Keywords found:**", item['explanation']['overlapped_keywords'])
                            st.write("**Overlap Ratio:**", item['explanation']['overlap_ratio'])
                        
                        st.divider()
            else:
                st.error(f"Error {res.status_code}: {res.text}")
                
        except requests.exceptions.ConnectionError:
            st.error(" Connection Error! Is the API running? Make sure to run 'uvicorn src.api:app' in another terminal.")