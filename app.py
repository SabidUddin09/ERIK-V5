import streamlit as st
import requests
from bs4 import BeautifulSoup
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from googlesearch import search

# ------------------ ERIK v5 ------------------
st.set_page_config(page_title="ERIK v5 - AI Academic Assistant", layout="wide")

st.title("🧠 ERIK v5 - Exceptional Resources & Intelligence Kernel")

# ------------------ Sidebar ------------------
st.sidebar.header("Features")
mode = st.sidebar.radio("Choose a feature:", [
    "Ask Question", 
    "Bangla Q&A",
    "Math Solver", 
    "Scientific Calculator", 
    "Quiz Generator", 
    "PDF/Text Analyzer", 
    "YouTube Class Search", 
    "Google Scholar Search", 
    "Graph Generator"
])

# ------------------ Ask Question ------------------
if mode == "Ask Question":
    query = st.text_input("Ask anything (English):")
    if st.button("Search & Answer"):
        st.info("Searching Google...")
        results = []
        try:
            for url in search(query, num_results=5):
                results.append(url)
        except:
            st.error("Error searching Google.")

        answer = ""
        for link in results:
            try:
                r = requests.get(link, timeout=3)
                soup = BeautifulSoup(r.text, 'html.parser')
                paragraphs = soup.find_all('p')
                for p in paragraphs[:2]:
                    answer += p.get_text() + "\n"
            except:
                continue

        if answer:
            st.markdown("**Answer from web sources:**")
            st.write(answer)
            st.markdown("**Top sources:**")
            for r in results:
                st.write(f"- {r}")
        else:
            st.warning("No answer found. Try rephrasing the question.")

# ------------------ Bangla Q&A ------------------
elif mode == "Bangla Q&A":
    query = st.text_input("যেকোনো প্রশ্ন করুন (বাংলায়):")
    if st.button("Search in Bangla"):
        st.info("গুগলে সার্চ করা হচ্ছে...")
        results = []
        try:
            for url in search(query, num_results=5, lang="bn"):
                results.append(url)
        except:
            st.error("Error searching Google.")

        answer = ""
        for link in results:
            try:
                r = requests.get(link, timeout=3)
                soup = BeautifulSoup(r.text, 'html.parser')
                paragraphs = soup.find_all('p')
                for p in paragraphs[:2]:
                    answer += p.get_text() + "\n"
            except:
                continue

        if answer:
            st.markdown("**ওয়েব থেকে উত্তর:**")
            st.write(answer)
            st.markdown("**উৎস লিঙ্কসমূহ:**")
            for r in results:
                st.write(f"- {r}")
        else:
            st.warning("কোনো উত্তর পাওয়া যায়নি। প্রশ্নটি অন্যভাবে লিখে চেষ্টা করুন।")

# ------------------ Math Solver ------------------
elif mode == "Math Solver":
    st.subheader("Math Problem Solver")
    problem = st.text_area("Enter a math problem (e.g., x**2 - 4):")
    if st.button("Solve"):
        try:
            x = sp.symbols('x')
            solution = sp.solve(problem, x)
            st.success(f"Solution: {solution}")
        except Exception as e:
            st.error(f"Error: {e}")

# ------------------ Scientific Calculator ------------------
elif mode == "Scientific Calculator":
    expr = st.text_input("Enter expression (e.g., sin(pi/2) + log(10)):")
    if st.button("Calculate"):
        try:
            result = sp.sympify(expr).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

# ------------------ Quiz Generator ------------------
elif mode == "Quiz Generator":
    st.subheader("Generate Multiple Choice Questions")
    topic = st.text_input("Enter topic:")
    num_q = st.number_input("Number of questions:", min_value=1, max_value=20, value=5)
    if st.button("Generate Quiz"):
        for i in range(num_q):
            st.write(f"Q{i+1}: This is a placeholder question about {topic}?")
            st.write("a) Option A  b) Option B  c) Option C  d) Option D")

# ------------------ PDF/Text Analyzer ------------------
elif mode == "PDF/Text Analyzer":
    st.subheader("Upload PDF or TXT")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf','txt'])
    if uploaded_file:
        text = ""
        if uploaded_file.type == "application/pdf":
            import fitz  # PyMuPDF
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
        else:
            text = str(uploaded_file.read(), "utf-8")
        st.text_area("Extracted Text", text, height=300)

# ------------------ YouTube Class Search ------------------
elif mode == "YouTube Class Search":
    st.subheader("Search YouTube Classes")
    keyword = st.text_input("Enter topic or class:")
    if st.button("Search YouTube"):
        st.info("Fetching top videos...")
        query = f"{keyword} site:youtube.com"
        links = []
        try:
            for url in search(query, num_results=5):
                if "watch" in url:
                    links.append(url)
        except:
            st.error("Error searching YouTube.")

        for l in links:
            video_id = l.split("v=")[-1]
            st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", width=300)
            st.write(f"[Watch Video]({l})")

# ------------------ Google Scholar Search ------------------
elif mode == "Google Scholar Search":
    st.subheader("Search Google Scholar")
    keyword = st.text_input("Enter research topic:")
    if st.button("Search Scholar"):
        st.info("Fetching top research papers...")
        query = f"{keyword} site:scholar.google.com"
        results = []
        try:
            for url in search(query, num_results=5):
                results.append(url)
        except:
            st.error("Error searching Scholar.")

        for r in results:
            st.write(f"- {r}")

# ------------------ Graph Generator ------------------
elif mode == "Graph Generator":
    st.subheader("Generate Graphs")
    func_input = st.text_input("Enter function in x (e.g., x**2 + 2*x - 3):")
    graph_type = st.radio("Graph Type:", ["2D", "3D"])
    if st.button("Plot Graph"):
        x = sp.symbols('x')
        func = sp.sympify(func_input)
        x_vals = np.linspace(-10, 10, 400)
        y_vals = [func.subs(x, val) for val in x_vals]

        if graph_type == "2D":
            plt.plot(x_vals, y_vals)
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title(f"Graph of {func_input}")
            st.pyplot(plt)
        else:
            from mpl_toolkits.mplot3d import Axes3D
            X = np.linspace(-5, 5, 100)
            Y = np.linspace(-5, 5, 100)
            X, Y = np.meshgrid(X, Y)
            Z = sp.lambdify((x,), func, "numpy")(X)  # works only for x functions
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis')
            st.pyplot(fig)
