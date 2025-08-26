import streamlit as st
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import docx
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import numpy as np
from youtubesearchpython import VideosSearch
from scholarly import scholarly
import io

# ------------------ ERIK v5 ------------------
st.set_page_config(page_title="ERIK v5 - AI Academic Assistant", layout="wide")

# ====== Language Toggle (English / Bangla) ======
LANG = st.sidebar.radio("Language / ভাষা", ["English", "বাংলা"], index=0)

T = {
    "English": {
        "title": "🧠 ERIK v5 - Exceptional Resources & Intelligence Kernel",
        "features": "Features",
        "feature_list": [
            "Ask Question",
            "Math Solver",
            "Scientific Calculator",
            "Quiz Generator",
            "PDF/Text Analyzer",
            "YouTube Class Search",
            "Google Scholar Search",
            "2D Graph Generator",
            "3D Surface Plotter",
        ],
        "ask_anything": "Ask anything:",
        "search_answer": "Search & Answer",
        "searching_msg": "Searching Google and generating answer...",
        "answer_web": "Answer from web sources:",
        "top_sources": "Top sources:",
        "no_answer": "No answer found. Try rephrasing the question.",
        "math_solver": "Math Problem Solver",
        "enter_problem": "Enter a math problem (symbolic or numeric):",
        "solve": "Solve",
        "solution": "Solution",
        "error": "Error",
        "quiz_gen": "Generate Multiple Choice Questions",
        "enter_topic": "Enter topic:",
        "num_questions": "Number of questions:",
        "upload": "Upload PDF or DOCX or TXT",
        "choose_file": "Choose a file",
        "extracted": "Extracted Text",
        "yt_search": "YouTube Class Finder",
        "enter_topic_or_class": "Enter topic or class:",
        "fetching_videos": "Fetching top videos...",
        "no_videos": "No videos found.",
        "scholar_search": "Google Scholar – Paper Search",
        "enter_query": "Enter topic / paper title / keywords:",
        "num_results": "Number of results:",
        "search": "Search",
        "authors": "Authors",
        "year": "Year",
        "link": "Link",
        "calculator": "Scientific Calculator",
        "calc_expr": "Enter expression (use sin, cos, tan, log, exp, pi, E):",
        "compute": "Compute",
        "result": "Result",
        "graph2d": "Generate 2D Graphs",
        "func_in_x": "Enter function in x (e.g., x**2 + 2*x - 3):",
        "plot": "Plot",
        "graph_of": "Graph of",
        "graph3d": "3D Surface Plotter",
        "func_in_xy": "Enter function in x,y (e.g., sin(x)*cos(y)):",
        "x_range": "x-range",
        "y_range": "y-range",
    },
    "বাংলা": {
        "title": "🧠 ERIK v5 - এক্সেপশনাল রিসোর্সেস & ইন্টেলিজেন্স কার্নেল",
        "features": "ফিচারসমূহ",
        "feature_list": [
            "প্রশ্ন করুন",
            "গণিত সমাধান",
            "সায়েন্টিফিক ক্যালকুলেটর",
            "কুইজ জেনারেটর",
            "PDF/টেক্সট বিশ্লেষক",
            "ইউটিউব ক্লাস সার্চ",
            "গুগল স্কলার সার্চ",
            "২ডি গ্রাফ জেনারেটর",
            "৩ডি সারফেস প্লটার",
        ],
        "ask_anything": "যেকোনো প্রশ্ন লিখুন:",
        "search_answer": "সার্চ করে উত্তর দিন",
        "searching_msg": "গুগলে সার্চ হচ্ছে এবং উত্তর প্রস্তুত করা হচ্ছে...",
        "answer_web": "ওয়েব সূত্র থেকে উত্তর:",
        "top_sources": "শীর্ষ সূত্রসমূহ:",
        "no_answer": "কোনো উত্তর পাওয়া যায়নি। প্রশ্নটি ভিন্নভাবে লিখে চেষ্টা করুন।",
        "math_solver": "গণিত সমস্যা সমাধান",
        "enter_problem": "গণিতের সমস্যা লিখুন (symbolic বা numeric):",
        "solve": "সমাধান করুন",
        "solution": "সমাধান",
        "error": "ত্রুটি",
        "quiz_gen": "মাল্টিপল চয়েস প্রশ্ন তৈরি",
        "enter_topic": "টপিক লিখুন:",
        "num_questions": "প্রশ্নের সংখ্যা:",
        "upload": "PDF, DOCX বা TXT আপলোড করুন",
        "choose_file": "ফাইল নির্বাচন করুন",
        "extracted": "উদ্ধৃত টেক্সট",
        "yt_search": "ইউটিউব ক্লাস ফাইন্ডার",
        "enter_topic_or_class": "টপিক/ক্লাস লিখুন:",
        "fetching_videos": "শীর্ষ ভিডিওগুলো আনা হচ্ছে...",
        "no_videos": "কোনো ভিডিও পাওয়া যায়নি।",
        "scholar_search": "গুগল স্কলার – পেপার সার্চ",
        "enter_query": "টপিক/পেপার শিরোনাম/কীওয়ার্ড লিখুন:",
        "num_results": "রেজাল্ট সংখ্যা:",
        "search": "সার্চ",
        "authors": "লেখকগণ",
        "year": "সাল",
        "link": "লিংক",
        "calculator": "সায়েন্টিফিক ক্যালকুলেটর",
        "calc_expr": "এক্সপ্রেশন লিখুন (sin, cos, tan, log, exp, pi, E ব্যবহার করুন):",
        "compute": "হিসাব করুন",
        "result": "ফলাফল",
        "graph2d": "২ডি গ্রাফ তৈরি",
        "func_in_x": "x এর ফাংশন লিখুন (যেমন: x**2 + 2*x - 3):",
        "plot": "গ্রাফ আঁকুন",
        "graph_of": "গ্রাফ:",
        "graph3d": "৩ডি সারফেস প্লটার",
        "func_in_xy": "x,y এর ফাংশন লিখুন (যেমন: sin(x)*cos(y)):",
        "x_range": "x-রেঞ্জ",
        "y_range": "y-রেঞ্জ",
    },
}

tr = T[LANG]

st.title(tr["title"])

# ------------------ Sidebar ------------------
st.sidebar.header(tr["features"])
mode = st.sidebar.radio(
    label="",
    options=tr["feature_list"],
)

# Utility: safe sympy environment for calculator and plots
SAFE = {
    **{k: getattr(sp, k) for k in [
        "sin", "cos", "tan", "asin", "acos", "atan",
        "log", "ln", "exp", "sqrt", "Abs", "pi", "E", "Symbol",
        "sinh", "cosh", "tanh", "asin", "acos", "atan",
    ]},
    **{k: getattr(sp, k) for k in ["Integer", "Rational", "Float"]},
}

# ------------------ Ask Question ------------------
if mode in ["Ask Question", "প্রশ্ন করুন"]:
    query = st.text_input(tr["ask_anything"]) 
    if st.button(tr["search_answer"]):
        st.info(tr["searching_msg"]) 
        results = []
        try:
            for url in search(query, num_results=5):
                results.append(url)
        except Exception:
            st.error(tr["error"] + ": Google search failed.")
        answer = ""
        for link in results:
            try:
                r = requests.get(link, timeout=5)
                soup = BeautifulSoup(r.text, 'html.parser')
                paragraphs = soup.find_all('p')
                for p in paragraphs[:3]:
                    answer += p.get_text() + "\n"
            except Exception:
                continue
        if answer:
            st.markdown(f"**{tr['answer_web']}**")
            st.write(answer)
            st.markdown(f"**{tr['top_sources']}**")
            for r in results:
                st.write(f"- {r}")
        else:
            st.warning(tr["no_answer"]) 

# ------------------ Math Solver ------------------
elif mode in ["Math Solver", "গণিত সমাধান"]:
    st.subheader(tr["math_solver"]) 
    problem = st.text_area(tr["enter_problem"]) 
    if st.button(tr["solve"]):
        try:
            x = sp.symbols('x')
            solution = sp.solve(problem, x)
            st.success(f"{tr['solution']}: {solution}")
        except Exception as e:
            st.error(f"{tr['error']}: {e}")

# ------------------ Scientific Calculator ------------------
elif mode in ["Scientific Calculator", "সায়েন্টিফিক ক্যালকুলেটর"]:
    st.subheader(tr["calculator"]) 
    expr = st.text_input(tr["calc_expr"], value="sin(pi/6) + log(10) + 2**3")
    if st.button(tr["compute"]):
        try:
            # parse with sympy
            parsed = sp.sympify(expr, locals=SAFE)
            result = sp.N(parsed)
            st.success(f"{tr['result']}: {result}")
        except Exception as e:
            st.error(f"{tr['error']}: {e}")

# ------------------ Quiz Generator ------------------
elif mode in ["Quiz Generator", "কুইজ জেনারেটর"]:
    st.subheader(tr["quiz_gen"]) 
    topic = st.text_input(tr["enter_topic"]) 
    num_q = st.number_input(tr["num_questions"], min_value=1, max_value=20, value=5)
    if st.button("Generate" if LANG=="English" else "তৈরি করুন"):
        for i in range(num_q):
            st.write(f"Q{i+1}: {'This is a placeholder question about' if LANG=='English' else 'এটি একটি প্লেসহোল্ডার প্রশ্ন'} {topic}?")
            st.write("a) Option A  b) Option B  c) Option C  d) Option D")

# ------------------ PDF/Text Analyzer ------------------
elif mode in ["PDF/Text Analyzer", "PDF/টেক্সট বিশ্লেষক"]:
    st.subheader(tr["upload"]) 
    uploaded_file = st.file_uploader(tr["choose_file"], type=['pdf','docx','txt'])
    if uploaded_file:
        text = ""
        try:
            if uploaded_file.type == "application/pdf":
                data = uploaded_file.read()
                doc = fitz.open(stream=data, filetype="pdf")
                for page in doc:
                    text += page.get_text()
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                document = docx.Document(uploaded_file)
                for para in document.paragraphs:
                    text += para.text + "\n"
            else:
                text = uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception as e:
            st.error(f"{tr['error']}: {e}")
        st.text_area(tr["extracted"], text, height=300)

# ------------------ YouTube Class Search (with thumbnails) ------------------
elif mode in ["YouTube Class Search", "ইউটিউব ক্লাস সার্চ"]:
    st.subheader(tr["yt_search"]) 
    keyword = st.text_input(tr["enter_topic_or_class"]) 
    if st.button("Search YouTube" if LANG=="English" else "ইউটিউব সার্চ"):
        st.info(tr["fetching_videos"]) 
        try:
            videos = VideosSearch(keyword, limit=8).result()
            results = videos.get('result', [])
            if not results:
                st.warning(tr["no_videos"]) 
            else:
                cols = st.columns(2)
                for idx, v in enumerate(results):
                    with cols[idx % 2]:
                        title = v.get('title', 'No title')
                        link = v.get('link', '')
                        thumbs = v.get('thumbnails', [])
                        thumb_url = thumbs[0]['url'] if thumbs else None
                        if thumb_url:
                            st.image(thumb_url, use_column_width=True)
                        st.markdown(f"**[{title}]({link})**")
                        dur = v.get('duration', '')
                        ch = v.get('channel', {}).get('name', '') if isinstance(v.get('channel'), dict) else v.get('channel', '')
                        st.caption(f"{ch} • {dur}")
                        if link:
                            st.video(link)
        except Exception as e:
            st.error(f"{tr['error']}: {e}")

# ------------------ Google Scholar Search ------------------
elif mode in ["Google Scholar Search", "গুগল স্কলার সার্চ"]:
    st.subheader(tr["scholar_search"]) 
    q = st.text_input(tr["enter_query"], value="transformer architecture attention")
    n = st.number_input(tr["num_results"], min_value=1, max_value=20, value=5)
    if st.button(tr["search"]):
        try:
            search_gen = scholarly.search_pubs(q)
            for i, pub in zip(range(int(n)), search_gen):
                bib = pub.get('bib', {})
                title = bib.get('title', 'Untitled')
                authors = ", ".join(bib.get('author', []))
                year = bib.get('pub_year', bib.get('year', ''))
                url = pub.get('eprint_url') or pub.get('pub_url') or pub.get('author_pub_url')
                st.markdown(f"**{title}**")
                st.write(f"{tr['authors']}: {authors}")
                st.write(f"{tr['year']}: {year}")
                if url:
                    st.write(f"{tr['link']}: {url}")
                st.divider()
        except Exception as e:
            st.error(f"{tr['error']}: {e}")

# ------------------ 2D Graph Generator ------------------
elif mode in ["2D Graph Generator", "২ডি গ্রাফ জেনারেটর"]:
    st.subheader(tr["graph2d"]) 
    func_input = st.text_input(tr["func_in_x"], value="sin(x) + x**2/10")
    if st.button(tr["plot"]):
        try:
            x = sp.symbols('x')
            func = sp.sympify(func_input, locals=SAFE)
            f_np = sp.lambdify(x, func, 'numpy')
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f_np(x_vals)
            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"{tr['graph_of']} {func_input}")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"{tr['error']}: {e}")

# ------------------ 3D Surface Plotter ------------------
elif mode in ["3D Surface Plotter", "৩ডি সারফেস প্লটার"]:
    st.subheader(tr["graph3d"]) 
    func_xy = st.text_input(tr["func_in_xy"], value="sin(x)*cos(y)")
    col1, col2 = st.columns(2)
    with col1:
        x_min, x_max = st.slider(tr["x_range"], -20.0, 20.0, (-6.28, 6.28))
    with col2:
        y_min, y_max = st.slider(tr["y_range"], -20.0, 20.0, (-6.28, 6.28))
    if st.button(tr["plot"]):
        try:
            x, y = sp.symbols('x y')
            f = sp.sympify(func_xy, locals=SAFE)
            f_np = sp.lambdify((x, y), f, 'numpy')
            X = np.linspace(x_min, x_max, 100)
            Y = np.linspace(y_min, y_max, 100)
            Xg, Yg = np.meshgrid(X, Y)
            Z = f_np(Xg, Yg)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(Xg, Yg, Z, linewidth=0, antialiased=True)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.set_title(f"z = {func_xy}")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"{tr['error']}: {e}")
