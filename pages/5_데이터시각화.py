import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import os

# 페이지 설정
st.set_page_config(page_title="데이터 시각화", layout="wide")
st.title("📊 데이터 시각화 예제")
st.write("matplotlib, seaborn, plotly를 활용한 다양한 시각화 예제입니다.")

# 한글 폰트 설정 (폰트 파일 직접 불러오기)
font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'NotoSans-Bold.ttf')
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 표시 수정
sns.set_style("whitegrid")

# 데이터 생성
np.random.seed(42)
months = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
sales_data = {
    '월': months,
    '판매액(만원)': np.random.randint(100, 500, 12),
    '방문객(명)': np.random.randint(1000, 3000, 12),
    '제품': np.random.choice(['A상품', 'B상품', 'C상품'], 12)
}
df = pd.DataFrame(sales_data)

# 추가 데이터: 카테고리별 판매
categories = ['의류', '식품', '전자제품', '가구', '도서']
category_sales = {
    '카테고리': categories,
    '판매액(만원)': [350, 280, 420, 310, 190]
}
df_category = pd.DataFrame(category_sales)

# 추가 데이터: 성별/연령대별 고객 분포
gender_age_data = {
    '나이대': ['10대', '20대', '30대', '40대', '50대', '60대'],
    '남성': [45, 120, 130, 100, 80, 40],
    '여성': [50, 140, 135, 110, 75, 45]
}
df_gender_age = pd.DataFrame(gender_age_data)

col1, col2 = st.columns(2)

# 1. Matplotlib - 라인 차트
with col1:
    st.subheader("📈 Matplotlib: 월별 판매액 추이")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['월'], df['판매액(만원)'], marker='o', linewidth=2, markersize=8, color='#2E86AB')
    ax.fill_between(range(len(df)), df['판매액(만원)'], alpha=0.3, color='#2E86AB')
    ax.set_title('월별 판매액 추이', fontsize=14, fontweight='bold')
    ax.set_xlabel('월', fontsize=12)
    ax.set_ylabel('판매액(만원)', fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# 2. Seaborn - 바 차트
with col2:
    st.subheader("📊 Seaborn: 카테고리별 판매액")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='카테고리', y='판매액(만원)', data=df_category, palette='Set2', ax=ax)
    ax.set_title('카테고리별 판매액', fontsize=14, fontweight='bold')
    ax.set_xlabel('카테고리', fontsize=12)
    ax.set_ylabel('판매액(만원)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

col3, col4 = st.columns(2)

# 3. Seaborn - 히트맵
with col3:
    st.subheader("🔥 Seaborn: 성별/연령대별 고객분포")
    df_pivot = df_gender_age.set_index('나이대')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(df_pivot, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': '고객수(명)'}, ax=ax)
    ax.set_title('성별/연령대별 고객 분포', fontsize=14, fontweight='bold')
    ax.set_xlabel('성별', fontsize=12)
    ax.set_ylabel('나이대', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)

# 4. Plotly - 대화형 라인 차트
with col4:
    st.subheader("📍 Plotly: 월별 방문객 수 (상호작용 가능)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['월'], 
        y=df['방문객(명)'],
        mode='lines+markers',
        name='방문객',
        line=dict(color='#A23B72', width=3),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title='월별 방문객 수',
        xaxis_title='월',
        yaxis_title='방문객(명)',
        hovermode='x unified',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

# 5. Plotly - 원형 차트
st.subheader("🥧 Plotly: 상품별 판매 비율")
product_sales = df.groupby('제품').size()
fig = px.pie(
    values=product_sales.values,
    names=product_sales.index,
    title='상품별 판매 비율',
    labels={'제품': '상품'},
    color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
)
st.plotly_chart(fig, use_container_width=True)

# 6. Plotly - 박스 플롯
st.subheader("📦 Plotly: 제품별 판매액 분포")
# 박스플롯용 추가 데이터 생성
box_data = []
for product in df['제품'].unique():
    sales_vals = np.random.randint(150, 500, 20)
    for val in sales_vals:
        box_data.append({'제품': product, '판매액(만원)': val})

df_box = pd.DataFrame(box_data)
fig = px.box(df_box, x='제품', y='판매액(만원)', title='제품별 판매액 분포',
             color='제품', color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
st.plotly_chart(fig, use_container_width=True)

# 데이터 표시
with st.expander("📋 원본 데이터 보기"):
    st.write("**월별 판매 데이터:**")
    st.dataframe(df, use_container_width=True)
    
    st.write("**카테고리별 판매 데이터:**")
    st.dataframe(df_category, use_container_width=True)
    
    st.write("**성별/연령대별 고객 분포:**")
    st.dataframe(df_gender_age, use_container_width=True)
