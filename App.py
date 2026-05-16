from langchain_groq import ChatGroq
import streamlit as st
import pandas as pd
import chromadb
import os

from sentence_transformers import SentenceTransformer

from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="University AI Assistant",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1 {
    color: #00ADB5;
    text-align: center;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.markdown("""
<h1>🎓 University AI Assistant</h1>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()

# =========================================================
# LOAD CHROMA DB
# =========================================================

#@st.cache_resource
def load_chroma():

    #BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    CHROMA_PATH ="./chroma_db2"
    

    #st.write("Chroma Path:", CHROMA_PATH)

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collections = {
        "students": client.get_collection("student_data"),
        "faculty": client.get_collection("faculty_data"),
        "courses": client.get_collection("courses_data"),
        "placements": client.get_collection("placements_data"),
        "research": client.get_collection("research_data")
    }

    return collections

#collections_map = load_chroma()
if "collections_map" not in st.session_state:

    st.session_state.collections_map = load_chroma()

collections_map = st.session_state.collections_map
# st.write("Students Count:", collections_map["students"].count())
# st.write("Placements Count:", collections_map["placements"].count())

# =========================================================
# LOAD LLM
# =========================================================

@st.cache_resource
def load_llm():
    return  ChatGroq(
    groq_api_key=st.secrets["GROQ_API_KEY"],
    model_name="llama-3.3-70b-versatile"
)

llm = load_llm()

# =========================================================
# MEMORY
# =========================================================

memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    return_messages=True
)

# =========================================================
# ROUTER PROMPT
# =========================================================

router_prompt = ChatPromptTemplate.from_template("""
You are a database router.

Available databases:
- students
- faculty
- courses
- placements
- research

Rules:
1. Return ONLY database names.
2. Return comma-separated values.
3. Do NOT explain anything.
4. Do NOT write sentences.
5. Output must be clean.

Examples:

Question:
Who got highest package?
Answer:
placements, students

Question:
Who teaches Deep Learning?
Answer:
faculty

Question:
Find AI research papers
Answer:
research

Question:
{question}

Answer:
""")

# =========================================================
# MAIN PROMPT
# =========================================================

main_prompt = ChatPromptTemplate.from_template("""
You are an intelligent university AI assistant.

You are given data retrieved from multiple university databases.

The databases may include:
- students
- faculty
- courses
- placements
- research

Your task:
1. Analyze relationships between databases.
2. Compare records intelligently.
3. Answer using logical reasoning.
4. Use ONLY provided context.
5. If numerical comparison is needed, calculate carefully.
6. If relationships exist across databases, explain them clearly.

Conversation History:
{chat_history}

Retrieved Context:
{context}

Question:
{question}

Answer:
""")

# =========================================================
# CHAINS
# =========================================================

router_chain = LLMChain(
    prompt=router_prompt,
    llm=llm
)

main_chain = LLMChain(
    prompt=main_prompt,
    llm=llm,
    memory=memory
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Filters")

selected_databases = st.sidebar.multiselect(
    "Select Databases",
    ["students", "faculty", "courses", "placements", "research"],
    default=["students", "faculty", "courses", "placements", "research"]
)

cgpa_filter = st.sidebar.slider(
    "Minimum CGPA",
    0.0,
    10.0,
    0.0
)

gender_filter = st.sidebar.selectbox(
    "Gender",
    ["All", "Male", "Female"]
)

branch_filter = st.sidebar.selectbox(
    "Branch",
    ["All", "CSE", "ECE", "EEE", "MECH", "CIVIL"]
)

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Database Stats")

try:
    st.sidebar.metric(
        "Students",
        collections_map["students"].count()
    )

    st.sidebar.metric(
        "Faculty",
        collections_map["faculty"].count()
    )

    st.sidebar.metric(
        "Courses",
        collections_map["courses"].count()
    )

    st.sidebar.metric(
        "Placements",
        collections_map["placements"].count()
    )

    st.sidebar.metric(
        "Research Papers",
        collections_map["research"].count()
    )

except:
    pass

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================

query = st.chat_input("Ask your question...")

# =========================================================
# PROCESS QUERY
# =========================================================

if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):

        with st.spinner("Searching databases..."):

            # =========================================
            # ROUTER
            # =========================================

            router_result = router_chain.invoke(
                {
                    "question": query
                }
            )

            selected_dbs = router_result["text"]

            selected_dbs = [
                db.strip().lower()
                for db in selected_dbs.split(",")
            ]

            # USE SIDEBAR FILTER
            selected_dbs = [
                db for db in selected_dbs
                if db in selected_databases
            ]

            st.info(f"Selected Databases: {selected_dbs}")

            # =========================================
            # QUERY EMBEDDING
            # =========================================

            query_embedding = embedding_model.encode(query).tolist()

            all_documents = []

            # =========================================
            # SEARCH DATABASES
            # =========================================

            for db in selected_dbs:

                if db not in collections_map:
                    continue

                collection = collections_map[db]

                where_clause = {}

                # =====================================
                # METADATA FILTERS
                # =====================================

                if db == "students":

                    conditions = []

                    if cgpa_filter > 0:
                        conditions.append(
                            {
                                "cgpa": {
                                    "$gte": cgpa_filter
                                }
                            }
                        )

                    if gender_filter != "All":
                        conditions.append(
                            {
                                "gender": {
                                    "$eq": gender_filter
                                }
                            }
                        )

                    if branch_filter != "All":
                        conditions.append(
                            {
                                "branch": {
                                    "$eq": branch_filter
                                }
                            }
                        )

                    if conditions:
                        where_clause = {
                            "$and": conditions
                        }

                # =====================================
                # QUERY VECTOR DB
                # =====================================

                try:

                    if where_clause:

                        result = collection.query(
                            query_embeddings=[query_embedding],
                            n_results=15,
                            where=where_clause
                            #st.write(result)
                        )

                    else:

                        result = collection.query(
                            query_embeddings=[query_embedding],
                            n_results=15
                        )
                    #st.write(result)

                    if (result["documents"]and len(result["documents"][0]) > 0):

                        retrieved_docs = result["documents"][0]

                        all_documents.extend(retrieved_docs)

                except Exception as e:
                    st.error(f"Error querying {db}: {e}")

            # =========================================
            # NO RESULTS
            # =========================================

            if not all_documents:

                response = "No matching data found."

            else:

                context = "\n\n".join(all_documents)

                result = main_chain.invoke(
                    {
                        "context": context,
                        "question": query
                    }
                )

                response = result["text"]

            # =========================================
            # SHOW RESPONSE
            # =========================================

            st.markdown(response)

            # =========================================
            # SHOW RETRIEVED DOCUMENTS
            # =========================================

            with st.expander("📄 Retrieved Documents"):

                for i, doc in enumerate(all_documents):

                    st.markdown(f"### Result {i+1}")
                    st.write(doc)
                    st.markdown("---")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
